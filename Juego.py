"""
Juego.py
--------
Módulo principal de la lógica del juego.
Incluye gestión de estados, música, sonidos, HUD mejorado y persistencia.
"""

import pyxel
import os
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe


class Juego:
    """
    Clase principal del juego.
    Coordina todas las entidades y la ejecución de la ventana.
    """

    def __init__(self):
        """Inicializa variables lógicas, pero NO la ventana todavía."""
        self.estado = "menu"        # "menu", "config", "juego"
        self.game_over = False

        # ---------------- CONFIGURACIÓN -----------------
        self.velocidades = [1.5, 2.0, 2.5, 3.0]
        self.velocidades_texto = ["Muy lenta", "Lenta", "Media", "Rápida"]
        self.config_vel_index = 2

        self.config_paquetes_index = 0
        self.num_paquetes = 1

        # ---------------- MENÚ / CONFIG CURSORES --------
        self.menu_opcion = 0       # 0 = JUGAR, 1 = SALIR
        self.config_cursor = 0

        # ---------------- MARCADORES --------------------
        self.puntuacion = 0
        self.fallos = 0
        self.record_actual = self.cargar_record()

        # ---------------- EFECTOS JEFE ------------------
        self.jefe_timer = 0
        self.jefe_duracion = 120
        self.shake = 0

        # ---------------- OBJETOS DEL JUEGO -------------
        # Las posiciones se calcularán bien al iniciar Pyxel,
        # pero definimos los objetos aquí.
        self.camion = Camion(1 * 8, 8 * 8)
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)
        self.jefe = Jefe(15 * 8, 3 * 8)

        self.pisos = [13 * 8, 8 * 8, 4 * 8]
        self.mario.pisos = self.pisos
        self.luigi.pisos = self.pisos

        self.paquetes = []

    # ==================================================
    #   ARRANQUE (NUEVO MÉTODO)
    # ==================================================
    def ejecutar(self):
        """Inicializa Pyxel, carga recursos y arranca el loop."""
        pyxel.init(256, 128, title="Mario Bros")

        # Cargar recursos y audio una vez iniciada la ventana
        pyxel.load("recursos.pyxres")
        self._init_sonidos()
        self._init_musica()

        # Objetos que requieren reinicio visual
        self.jefe.desaparecer()

        pyxel.run(self.update, self.draw)

    # ==================================================
    #   SONIDO Y DATOS
    # ==================================================
    def _init_sonidos(self):
        # Sfx 0: Entrega
        pyxel.sound(0).set("c3e3g3c4", "t", "6", "vffn", 25)
        # Sfx 1: Fallo
        pyxel.sound(1).set("c2c1", "n", "77", "vffn", 25)
        # Sfx 2: Game Over
        pyxel.sound(2).set("c3g2e2c2", "s", "6", "vffn", 30)

    def _init_musica(self):
        # Melodía
        pyxel.sound(10).set("e3e3r c3e3g3r g2r c3g2e2 a2b2a2g2", "s", "4", "nnnf", 11)
        pyxel.sound(11).set("c3r g2e2a2b2 a2g2e3g3 a3f3g3e3 c3d3b2c3", "s", "4", "nnnf", 11)
        # Bajo
        pyxel.sound(12).set("c2r g1r c2r g1r f1r c2r f1r c2r", "t", "6", "n", 11)

    def cargar_record(self) -> int:
        archivo = "record.txt"
        if os.path.exists(archivo):
            try:
                with open(archivo, "r") as f:
                    return int(f.read())
            except ValueError: return 0
        return 0

    def guardar_record(self):
        if self.puntuacion > self.record_actual:
            self.record_actual = self.puntuacion
            try:
                with open("record.txt", "w") as f:
                    f.write(str(self.record_actual))
            except IOError: pass

    # ==================================================
    #   UPDATE
    # ==================================================
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.estado == "menu":
            self._update_menu()
        elif self.estado == "config":
            self._update_config()
        elif self.estado == "juego":
            self._update_juego()

    def _update_menu(self):
        # Navegación vertical
        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_opcion = (self.menu_opcion - 1) % 2
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_opcion = (self.menu_opcion + 1) % 2

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_opcion == 0:
                self.estado = "config"
            elif self.menu_opcion == 1:
                pyxel.quit()

    def _update_config(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.config_cursor = (self.config_cursor - 1) % 4
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.config_cursor = (self.config_cursor + 1) % 4

        # Ajustar valores
        if self.config_cursor == 0:
            if pyxel.btnp(pyxel.KEY_LEFT): self.config_vel_index = (self.config_vel_index - 1) % 4
            if pyxel.btnp(pyxel.KEY_RIGHT): self.config_vel_index = (self.config_vel_index + 1) % 4
        elif self.config_cursor == 1:
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_paquetes_index = 1 - self.config_paquetes_index

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.config_cursor == 2: self.iniciar_partida()
            elif self.config_cursor == 3:
                pyxel.stop()
                self.estado = "menu"

    def iniciar_partida(self):
        self.puntuacion = 0
        self.fallos = 0
        self.game_over = False
        self.record_actual = self.cargar_record()

        self.camion.carga = 0
        self.camion.estado = Camion.PARADO
        self.camion.x = 1 * 8
        self.camion.y = 8 * 8
        self.camion.reparto_terminado = False

        self.mario.piso = 0
        self.luigi.piso = 0
        self.mario.y = self.pisos[0]
        self.luigi.y = self.pisos[0]

        self.jefe.desaparecer()
        self.jefe_timer = 0
        self.shake = 0

        Paquete.VX = self.velocidades[self.config_vel_index]
        self.num_paquetes = 1 if self.config_paquetes_index == 0 else 2
        self._crear_paquetes_segun_config()

        self.estado = "juego"
        pyxel.play(0, [10, 11], loop=True)
        pyxel.play(1, [12, 12], loop=True)

    def _crear_paquetes_segun_config(self):
        self.paquetes = []
        p1 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
        p1.reiniciar_salida()
        self.paquetes.append(p1)
        if self.num_paquetes == 2:
            p2 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
            p2.reiniciar_salida()
            p2.activo = False
            self.paquetes.append(p2)

    def _update_juego(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R): self.iniciar_partida()
            return

        if self._update_jefe_activo(): return
        if self._update_camion(): return

        self._update_personajes()
        self._update_paquetes()

        if self.fallos >= 3:
            self.game_over = True
            self.guardar_record()
            pyxel.stop()
            pyxel.play(0, 2)

    def _update_paquetes(self):
        if self.num_paquetes == 2 and len(self.paquetes) > 1:
            p1, p2 = self.paquetes[0], self.paquetes[1]
            if not p2.activo and p1.piso == 2 and p1.x <= Paquete.COL_COL_CONTACTO_DER * 8:
                p2.reiniciar_salida()
                p2.activo = True
        for p in self.paquetes: p.update(self.mario, self.luigi, self)

    def _update_jefe_activo(self):
        if self.jefe_timer <= 0: return False
        self.jefe_timer -= 1
        self.jefe.update()
        for p in self.paquetes:
            if p.estado == "caida_fallo": p.update(self.mario, self.luigi, self)
        self.shake = 3
        if self.jefe_timer <= 0:
            self.jefe.desaparecer()
            self.shake = 0
            for p in self.paquetes:
                if not p.activo:
                    p.reiniciar_salida()
                    p.activo = True
        return True

    def _update_camion(self):
        self.camion.update()
        if self.camion.reparto_terminado:
            self.camion.reparto_terminado = False
            self._crear_paquetes_segun_config()
        return self.camion.estado == Camion.FUERA

    def _update_personajes(self):
        if pyxel.btnp(pyxel.KEY_UP): self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN): self.mario.mover_abajo()
        if pyxel.btnp(pyxel.KEY_W): self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S): self.luigi.mover_abajo()

    def invocar_jefe(self):
        self.jefe.aparecer()
        self.jefe_timer = self.jefe_duracion
        self.shake = 3
        pyxel.play(0, 1)

    # ==================================================
    #   DRAW
    # ==================================================
    def draw(self):
        if self.estado == "menu":
            self._draw_menu()
        elif self.estado == "config":
            self._draw_config()
        elif self.estado == "juego":
            self._draw_juego()

    def _draw_menu(self):
        pyxel.cls(0)

        # TÍTULO
        titulo = "PROYECTO SUPER MARIO"
        x_tit = (pyxel.width - len(titulo)*4) // 2
        pyxel.text(x_tit, 30, titulo, 10) # 10 es amarillo

        # OPCIONES CENTRADAS
        opciones = ["JUGAR", "SALIR"]
        y_inicial = 70

        for i, txt in enumerate(opciones):
            es_sel = (i == self.menu_opcion)

            # Decoración de selección
            prefix = "> " if es_sel else "  "
            texto_completo = prefix + txt + (" <" if es_sel else "  ")
            color = 7 if es_sel else 13 # Blanco si seleccionado, gris si no

            # Cálculo de centro exacto
            x_txt = (pyxel.width - len(texto_completo)*4) // 2

            pyxel.text(x_txt, y_inicial + i * 15, texto_completo, color)

        # (Se ha eliminado el texto de Sprint 5)

    def _draw_config(self):
        pyxel.cls(0)
        t = "CONFIGURACION"
        pyxel.text((pyxel.width - len(t)*4)//2, 20, t, 11)

        vt = self.velocidades_texto[self.config_vel_index]
        np = "1" if self.config_paquetes_index == 0 else "2"
        items = [f"Velocidad: {vt}", f"Paquetes: {np}", "EMPEZAR PARTIDA", "VOLVER AL MENU"]

        y = 50
        for i, txt in enumerate(items):
            c, p = (10, "> ") if i == self.config_cursor else (7, "  ")
            pyxel.text(40, y + i * 10, p + txt, c)

    def _draw_juego(self):
        pyxel.cls(7)
        dx = pyxel.rndi(-self.shake, self.shake) if self.jefe_timer > 0 else 0
        dy = pyxel.rndi(-self.shake, self.shake) if self.jefe_timer > 0 else 0

        # Fondo
        pyxel.bltm(dx, dy, 0, 0, 0, pyxel.tilemaps[0].width, pyxel.tilemaps[0].height, colkey=7)

        # --- HUD MEJORADO ---
        # Caja contenedora a la derecha
        hud_x, hud_y = 190, 2
        hud_w, hud_h = 60, 45

        # Fondo semi-transparente (simulado con color sólido oscuro) y borde
        pyxel.rect(hud_x, hud_y, hud_w, hud_h, 0) # Fondo negro
        pyxel.rectb(hud_x, hud_y, hud_w, hud_h, 13) # Borde gris

        # Etiquetas y valores alineados
        # SCORE
        pyxel.text(hud_x + 4, hud_y + 4, "SCORE", 6) # Etiqueta gris claro
        pyxel.text(hud_x + 35, hud_y + 4, str(self.puntuacion), 7) # Valor blanco

        # HIGH SCORE
        pyxel.text(hud_x + 4, hud_y + 14, "HIGH", 6)
        pyxel.text(hud_x + 35, hud_y + 14, str(self.record_actual), 10) # Valor amarillo

        # FALLOS (Cruces)
        pyxel.text(hud_x + 4, hud_y + 24, "MISS", 6)
        for i in range(3):
            col = 8 if i < self.fallos else 1 # Rojo si fallo, Azul oscuro si no
            txt = "X" if i < self.fallos else "-"
            pyxel.text(hud_x + 35 + (i*6), hud_y + 24, txt, col)

        # CAMION
        pyxel.text(hud_x + 4, hud_y + 34, "LOAD", 6)
        # Barra de progreso simple
        pyxel.rect(hud_x + 28, hud_y + 35, 24, 4, 1) # Fondo barra
        ancho_barra = int((self.camion.carga / 8) * 24)
        pyxel.rect(hud_x + 28, hud_y + 35, ancho_barra, 4, 11) # Relleno verde

        # --- DIBUJADO OBJETOS ---
        self.camion.draw()
        pyxel.blt(self.luigi.x + dx, self.luigi.y + dy, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x + dx, self.mario.y + dy, *self.mario.sprite_mario)

        for p in self.paquetes: p.draw()
        self.jefe.draw()

        if self.camion.estado == Camion.FUERA:
            msg = "DESCANSO..."
            pyxel.text((pyxel.width - len(msg)*4)//2, pyxel.height//2, msg, 0)
            pyxel.text((pyxel.width - len(msg)*4)//2 - 1, pyxel.height//2 - 1, msg, 8)

        if self.game_over:
            self._draw_game_over()

    def _draw_game_over(self):
        # Pantalla oscurecida
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)

        cx, cy = pyxel.width//2, pyxel.height//2

        t1 = "GAME OVER"
        pyxel.text(cx - len(t1)*2, cy - 20, t1, 8)

        t2 = f"SCORE: {self.puntuacion}"
        pyxel.text(cx - len(t2)*2, cy, t2, 7)

        if self.puntuacion >= self.record_actual and self.puntuacion > 0:
            t3 = "!NUEVO RECORD!"
            pyxel.text(cx - len(t3)*2, cy + 10, t3, 10)

        t4 = "PULSA R"
        pyxel.text(cx - len(t4)*2, cy + 30, t4, 6)