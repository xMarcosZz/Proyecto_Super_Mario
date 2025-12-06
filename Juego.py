"""
Juego.py — versión corregida y funcional
---------------------------------------
Incluye:
• Menú principal
• Menú de configuración (velocidad + número de paquetes)
• Juego completo
• Game over con reinicio
• Eliminado KEY_ENTER (solo KEY_RETURN)
"""

import pyxel
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe


class Juego:

    def __init__(self):
        pyxel.load("recursos.pyxres")

        # ----- ESTADOS DEL JUEGO -----
        self.estado_juego = "menu"   # menu → config → jugando → gameover

        # ----- MENÚ -----
        self.menu_index = 0
        self.menu_opciones = ["JUGAR", "SALIR"]

        # ----- CONFIGURACIÓN -----
        self.config_vel_index = 1       # velocidad por defecto
        self.config_velocidades = [1.5, 2.5, 3.5, 4.5]
        self.config_num_paquetes = 1    # 1 o 2 paquetes
        self.config_submenu = 0         # 0 = velocidad, 1 = nº paquetes, 2 = aceptar

        # ----- MARCADORES -----
        self.puntuacion = 0
        self.fallos = 0

        self.game_over = False
        self.jefe_timer = 0
        self.jefe_duracion = 120
        self.shake = 0

        # ----- OBJETOS DEL JUEGO -----
        self.camion = Camion(1 * 8, 8 * 8)
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)

        # Se crearán en _crear_paquetes_iniciales()
        self.paquetes = []

        self.jefe = Jefe(15 * 8, 3 * 8)
        self.jefe.desaparecer()

        self.pisos = [13 * 8, 8 * 8, 4 * 8]
        self.mario.pisos = self.pisos
        self.luigi.pisos = self.pisos

    # ============================================================
    #                      UPDATE GENERAL
    # ============================================================

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.estado_juego == "menu":
            self._update_menu()
            return

        if self.estado_juego == "config":
            self._update_config()
            return

        if self.estado_juego == "gameover":
            self._update_game_over()
            return

        if self.estado_juego == "jugando":
            self._update_jugando()
            return

    # ============================================================
    #                        MENÚ PRINCIPAL
    # ============================================================

    def _update_menu(self):

        # Mover cursor en el menú
        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_index = (self.menu_index - 1) % len(self.menu_opciones)

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_index = (self.menu_index + 1) % len(self.menu_opciones)

        # Selección con ENTER (RETURN)
        if pyxel.btnp(pyxel.KEY_RETURN):
            opcion = self.menu_opciones[self.menu_index]

            if opcion == "JUGAR":
                self.estado_juego = "config"

            elif opcion == "SALIR":
                pyxel.quit()

    # ============================================================
    #                  SUBMENÚ DE CONFIGURACIÓN
    # ============================================================

    def _update_config(self):

        if pyxel.btnp(pyxel.KEY_UP):
            self.config_submenu = (self.config_submenu - 1) % 3

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.config_submenu = (self.config_submenu + 1) % 3

        # Ajustar valores
        if self.config_submenu == 0:  # velocidad
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.config_vel_index = max(0, self.config_vel_index - 1)
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_vel_index = min(len(self.config_velocidades) - 1,
                                            self.config_vel_index + 1)

        elif self.config_submenu == 1:  # nº paquetes
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.config_num_paquetes = 1
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_num_paquetes = 2

        # Confirmar selección
        if self.config_submenu == 2 and pyxel.btnp(pyxel.KEY_RETURN):
            self._configurar_velocidad_paquetes()
            self.reiniciar_partida(desde_menu=True)
            self.estado_juego = "jugando"

    # ============================================================
    #                     UPDATE DE JUEGO REAL
    # ============================================================

    def _update_jugando(self):

        # GAME OVER por fallos
        if self.fallos >= 3:
            self.estado_juego = "gameover"
            return

        # JEFE activo (pausa)
        if self._update_jefe_activo():
            return

        # CAMIÓN
        if self._update_camion():
            return

        # PERSONAJES
        self._update_personajes()

        # PAQUETES
        for paquete in self.paquetes:
            paquete.update(self.mario, self.luigi, self)

        # JEFE animación
        self.jefe.update()

    # ============================================================
    #                     GAME OVER Y REINICIO
    # ============================================================

    def _update_game_over(self):

        if pyxel.btnp(pyxel.KEY_R):
            self.reiniciar_partida(desde_menu=True)
            self.estado_juego = "menu"

    # ============================================================
    #                         DIBUJADO
    # ============================================================

    def draw(self):
        pyxel.cls(7)

        if self.estado_juego == "menu":
            return self._draw_menu()

        if self.estado_juego == "config":
            return self._draw_config()

        # Temblor
        dx = dy = 0
        if self.jefe_timer > 0:
            dx = pyxel.rndi(-self.shake, self.shake)
            dy = pyxel.rndi(-self.shake, self.shake)

        # Tilemap
        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height
        pyxel.bltm(dx, dy, 0, 0, 0, ancho, alto, colkey=7)

        # HUD
        pyxel.text(200, 2, f"Puntos: {self.puntuacion}", 7)
        pyxel.text(200, 10, f"Fallos: {self.fallos}", 8)
        pyxel.text(200, 18, f"Camion: {self.camion.carga}/8", 7)

        # Cruces de fallos
        self._draw_cruces()

        # Objetos
        self.camion.draw()
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite_mario)

        for p in self.paquetes:
            p.draw()

        self.jefe.draw()

        if self.estado_juego == "gameover":
            self._draw_game_over()

    # ============================================================
    #               MÉTODOS AUXILIARES - CONFIGURACIÓN
    # ============================================================

    def _configurar_velocidad_paquetes(self):
        nueva_vel = self.config_velocidades[self.config_vel_index]
        for paquete in self.paquetes:
            paquete.VX = nueva_vel

    def _crear_paquetes_iniciales(self):
        self.paquetes = [
            Paquete(32 * 8, 13 * 8)
        ]
        if self.config_num_paquetes == 2:
            self.paquetes.append(
                Paquete(32 * 8 + 50, 13 * 8)
            )

    # ============================================================
    #                  MÉTODOS AUXILIARES VARIOS
    # ============================================================

    def _update_jefe_activo(self):
        if self.jefe_timer <= 0:
            return False

        self.jefe_timer -= 1
        self.jefe.update()

        for p in self.paquetes:
            p.update(self.mario, self.luigi, self)

        self.shake = 3

        if self.jefe_timer <= 0:
            self.jefe.desaparecer()
            self.shake = 0

        return True

    def _update_camion(self):
        self.camion.update()

        if self.camion.reparto_terminado:
            self.camion.reparto_terminado = False
            for p in self.paquetes:
                p.reiniciar_salida()

        if self.camion.estado == "fuera":
            return True

        return False

    def _update_personajes(self):

        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover_abajo()

        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover_abajo()

    # ============================================================
    #                         DIBUJADO AUXILIAR
    # ============================================================

    def _draw_menu(self):
        pyxel.cls(0)
        pyxel.text(85, 30, "SUPER MARIO LOGISTICS", 10)

        opciones_y = 80
        for i, op in enumerate(self.menu_opciones):
            color = 7 if i == self.menu_index else 5
            pyxel.text(110, opciones_y + i * 12, op, color)

        pyxel.text(110, 140, "ENTER para seleccionar", 13)

    def _draw_config(self):
        pyxel.cls(1)
        pyxel.text(70, 20, "CONFIGURACION DE PARTIDA", 7)

        # Velocidad
        vel_lbl = f"VELOCIDAD: {self.config_velocidades[self.config_vel_index]}"
        col = 10 if self.config_submenu == 0 else 7
        pyxel.text(60, 60, vel_lbl, col)

        # Nº paquetes
        num_lbl = f"PAQUETES: {self.config_num_paquetes}"
        col = 10 if self.config_submenu == 1 else 7
        pyxel.text(60, 80, num_lbl, col)

        # Confirmar
        col = 10 if self.config_submenu == 2 else 7
        pyxel.text(60, 110, "EMPEZAR PARTIDA (ENTER)", col)

    def _draw_cruces(self):
        posiciones_x = [17 * 8, 19 * 8, 21 * 8]
        for i in range(min(self.fallos, 3)):
            pyxel.text(posiciones_x[i], 0, "X", 8)

    def _draw_game_over(self):
        pyxel.rect(0, 0, 240, 180, 0)
        pyxel.text(100, 70, "GAME OVER", pyxel.frame_count % 15)
        pyxel.text(80, 100, "Pulsa R para volver al menu", 7)

    # ============================================================
    #                     EVENTOS ESPECIALES
    # ============================================================

    def invocar_jefe(self):
        self.jefe.aparecer()
        self.jefe_timer = self.jefe_duracion
        self.shake = 3

    def reiniciar_partida(self, desde_menu=False):

        self.puntuacion = 0
        self.fallos = 0
        self.game_over = False

        # Reset camión
        self.camion.carga = 0
        self.camion.estado = "parado"
        self.camion.x = 1 * 8
        self.camion.y = 8 * 8
        self.camion.reparto_terminado = False

        # Reset personajes
        self.mario.piso = 0
        self.luigi.piso = 0
        self.mario.y = self.pisos[0]
        self.luigi.y = self.pisos[0]

        # Reset jefe
        self.jefe.desaparecer()
        self.jefe_timer = 0
        self.shake = 0

        # Crear paquetes según configuración
        self._crear_paquetes_iniciales()

