"""
Juego.py — Lógica principal del juego
Incluye:
- Menú principal
- Menú de configuración
- Partida
- Control de camión, paquetes, jefe y personajes
"""

import pyxel
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe


class Juego:

    # =====================================================
    #                   INICIALIZACIÓN
    # =====================================================

    def __init__(self):
        pyxel.load("recursos.pyxres")

        # ---------------- ESTADO DEL JUEGO ----------------
        self.estado = "menu"     # "menu", "config", "juego"
        self.game_over = False

        # ---------------- CONFIGURACIÓN -------------------
        self.velocidades = [1.5, 2.0, 2.5, 3.0]
        self.velocidades_texto = ["Muy lenta", "Lenta", "Media", "Rápida"]
        self.config_vel_index = 2

        self.config_paquetes_index = 0   # 0 = 1 paquete, 1 = 2 paquetes
        self.num_paquetes = 1

        # ---------------- CURSORES ------------------------
        self.menu_opcion = 0       # 0 = JUGAR, 1 = SALIR
        self.config_cursor = 0     # 0 vel, 1 paquetes, 2 empezar, 3 volver

        # ---------------- MARCADORES ----------------------
        self.puntuacion = 0
        self.fallos = 0

        # ---------------- JEFE ----------------------------
        self.jefe_timer = 0
        self.jefe_duracion = 120       # 2 segundos
        self.shake = 0

        self.jefe = Jefe(15 * 8, 3 * 8)
        self.jefe.desaparecer()

        # ---------------- PERSONAJES ----------------------
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)

        self.pisos = [13 * 8, 8 * 8, 4 * 8]
        self.mario.pisos = self.pisos
        self.luigi.pisos = self.pisos

        # ---------------- CAMIÓN --------------------------
        self.camion = Camion(1 * 8, 8 * 8)

        # ---------------- PAQUETES ------------------------
        self.paquetes = []


    # =====================================================
    #                   UPDATE GENERAL
    # =====================================================

    def update(self):

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.estado == "menu":
            self._update_menu()
            return

        if self.estado == "config":
            self._update_config()
            return

        if self.estado == "juego":
            self._update_juego()
            return


    # =====================================================
    #                   MENÚ PRINCIPAL
    # =====================================================

    def _update_menu(self):

        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_opcion = (self.menu_opcion - 1) % 2

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_opcion = (self.menu_opcion + 1) % 2

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_opcion == 0:
                self.estado = "config"
            else:
                pyxel.quit()


    # =====================================================
    #               MENÚ CONFIGURACIÓN
    # =====================================================

    def _update_config(self):

        if pyxel.btnp(pyxel.KEY_UP):
            self.config_cursor = (self.config_cursor - 1) % 4

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.config_cursor = (self.config_cursor + 1) % 4

        # Ajustar velocidad
        if self.config_cursor == 0:
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.config_vel_index = (self.config_vel_index - 1) % len(self.velocidades)
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_vel_index = (self.config_vel_index + 1) % len(self.velocidades)

        # Ajustar nº paquetes
        if self.config_cursor == 1:
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_paquetes_index = 1 - self.config_paquetes_index

        # Seleccionar opción
        if pyxel.btnp(pyxel.KEY_RETURN):

            # EMPEZAR PARTIDA
            if self.config_cursor == 2:
                self.iniciar_partida()

            # VOLVER
            elif self.config_cursor == 3:
                self.estado = "menu"


    # =====================================================
    #                 INICIAR PARTIDA
    # =====================================================

    def iniciar_partida(self):

        # Reset marcadores
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

        # Aplicar velocidad configurada
        Paquete.VX = self.velocidades[self.config_vel_index]

        # Nº de paquetes
        self.num_paquetes = 1 if self.config_paquetes_index == 0 else 2

        # Crear paquetes
        self._crear_paquetes()

        self.estado = "juego"


    def _crear_paquetes(self):
        """Crea 1 o 2 paquetes según la configuración."""
        self.paquetes = []

        # Paquete principal
        p1 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
        p1.reiniciar_salida()
        self.paquetes.append(p1)

        if self.num_paquetes == 2:
            # Segundo paquete: empieza apagado
            p2 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
            p2.reiniciar_salida()
            p2.activo = False
            self.paquetes.append(p2)


    # =====================================================
    #                     UPDATE JUEGO
    # =====================================================

    def _update_juego(self):

        # Game over
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.iniciar_partida()
            return

        # Jefe activo → pausar todo excepto caída
        if self._update_jefe_activo():
            return

        # Camión saliendo o volviendo → pausa
        if self._update_camion():
            return

        # Controles
        self._update_personajes()

        # Paquetes
        self._update_paquetes()

        # ¿game over?
        if self.fallos >= 3:
            self.game_over = True


    # =====================================================
    #                UPDATE PAQUETES (CORREGIDO)
    # =====================================================

    def _update_paquetes(self):

        MIN_DIST = 40   # Distancia mínima entre paquetes

        # 2 PAQUETES → activar 2º cuando 1º llegue a piso 1
        if self.num_paquetes == 2:
            p1 = self.paquetes[0]
            p2 = self.paquetes[1]

            if (not p2.activo
                and p1.piso == 1
                and p1.x <= 17 * 8):
                p2.reiniciar_salida()
                p2.activo = True

            # Mantener separación mínima
            if p1.activo and p2.activo and p1.piso == p2.piso:

                # p1 delante, p2 detrás
                if p1.x > p2.x and (p1.x - p2.x) < MIN_DIST:
                    p2.x = p1.x - MIN_DIST
                    p2.x_real = float(p2.x)

                # p2 delante, p1 detrás
                if p2.x > p1.x and (p2.x - p1.x) < MIN_DIST:
                    p1.x = p2.x - MIN_DIST
                    p1.x_real = float(p1.x)

        # Actualizar movimiento de cada paquete
        for p in self.paquetes:
            p.update(self.mario, self.luigi, self)


    # =====================================================
    #                UPDATE JEFE ACTIVO
    # =====================================================

    def _update_jefe_activo(self):

        if self.jefe_timer <= 0:
            return False

        self.jefe_timer -= 1
        self.jefe.update()

        # Solo actualizamos paquetes que caen
        for p in self.paquetes:
            if p.estado == "caida_fallo":
                p.update(self.mario, self.luigi, self)

        self.shake = 3

        if self.jefe_timer <= 0:
            self.jefe.desaparecer()
            self.shake = 0

            # Respawn seguro
            for p in self.paquetes:
                if not p.activo:
                    p.reiniciar_salida()
                    p.activo = True

        return True


    # =====================================================
    #                  UPDATE CAMIÓN
    # =====================================================

    def _update_camion(self):

        self.camion.update()

        if self.camion.reparto_terminado:
            self.camion.reparto_terminado = False

            for i, p in enumerate(self.paquetes):
                p.reiniciar_salida()
                p.activo = True
                if i == 1 and self.num_paquetes == 2:
                    p.activo = False   # segundo espera activación

        return self.camion.estado == "fuera"


    # =====================================================
    #                 UPDATE PERSONAJES
    # =====================================================

    def _update_personajes(self):

        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover_abajo()

        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover_abajo()


    # =====================================================
    #                     DIBUJADO
    # =====================================================

    def draw(self):

        if self.estado == "menu":
            self._draw_menu()
        elif self.estado == "config":
            self._draw_config()
        elif self.estado == "juego":
            self._draw_juego()


    # ------------------- MENÚ ---------------------

    def _draw_menu(self):
        pyxel.cls(0)

        titulo = "PROYECTO SUPER MARIO"
        tx = (pyxel.width - len(titulo) * 4) // 2
        pyxel.text(tx, 20, titulo, 10)

        opciones = ["JUGAR", "SALIR"]
        y_base = 60
        x_base = 100

        for i, t in enumerate(opciones):
            color = 10 if i == self.menu_opcion else 7
            pref = "> " if i == self.menu_opcion else "  "
            pyxel.text(x_base - 20, y_base + i * 10, pref + t, color)


    # ---------------- CONFIG -----------------------

    def _draw_config(self):
        pyxel.cls(0)

        pyxel.text(85, 20, "CONFIGURACION", 11)

        vel = self.velocidades_texto[self.config_vel_index]
        num = "1" if self.config_paquetes_index == 0 else "2"

        lineas = [
            f"Velocidad: {vel}",
            f"Paquetes: {num}",
            "EMPEZAR PARTIDA",
            "VOLVER AL MENU"
        ]

        y = 55
        for i, t in enumerate(lineas):
            color = 10 if i == self.config_cursor else 7
            pref = "> " if i == self.config_cursor else "  "
            pyxel.text(40, y + i * 10, pref + t, color)


    # ---------------- JUEGO ------------------------

    def _draw_juego(self):
        pyxel.cls(7)

        dx = dy = 0
        if self.jefe_timer > 0:
            dx = pyxel.rndi(-self.shake, self.shake)
            dy = pyxel.rndi(-self.shake, self.shake)

        # Fondo
        pyxel.bltm(dx, dy, 0, 0, 0, pyxel.tilemaps[0].width, pyxel.tilemaps[0].height, colkey=7)

        # HUD
        pyxel.text(200, 2, f"Puntos: {self.puntuacion}", 1)
        pyxel.text(200, 10, f"Fallos: {self.fallos}", 8)
        pyxel.text(200, 18, f"Camion: {self.camion.carga}/8", 1)

        self._draw_fallos()

        # Objetos
        self.camion.draw()
        pyxel.blt(self.luigi.x + dx, self.luigi.y + dy, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x + dx, self.mario.y + dy, *self.mario.sprite_mario)

        for p in self.paquetes:
            p.draw()

        self.jefe.draw()

        # Mensaje de reparto centrado
        if self.camion.estado == "fuera":
            msg = "EL CAMION ESTA EN REPARTO..."
            pyxel.text((256 - len(msg) * 4) // 2, 120, msg, 8)

        if self.game_over:
            self._draw_game_over()


    def _draw_fallos(self):
        pos = [17 * 8, 19 * 8, 21 * 8]
        for i in range(min(self.fallos, 3)):
            pyxel.text(pos[i], 0, "X", 8)


    def _draw_game_over(self):

        pyxel.rect(0, 0, 256, 256, 0)

        msg1 = "GAME OVER"
        msg2 = "Pulsa R para reiniciar"

        pyxel.text((256 - len(msg1) * 4) // 2, 100, msg1, 10)
        pyxel.text((256 - len(msg2) * 4) // 2, 120, msg2, 7)


    # =====================================================
    #                EVENTO: APARICIÓN DEL JEFE
    # =====================================================

    def invocar_jefe(self):
        self.jefe.aparecer()
        self.jefe_timer = self.jefe_duracion
        self.shake = 3
