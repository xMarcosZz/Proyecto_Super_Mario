"""
Juego.py
--------
Módulo principal de la lógica del juego.

Estados principales:
- "menu"    : menú inicial (JUGAR / SALIR)
- "config"  : menú de configuración (velocidad, nº de paquetes)
- "juego"   : partida en marcha
"""

import pyxel
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe


class Juego:
    """
    Clase principal del juego.

    Coordina:
    - Menú y configuración
    - Camión, personajes, paquetes y jefe
    - Puntuación, fallos y game over
    """

    def __init__(self):
        """Inicializa recursos, variables de estado y objetos del juego."""
        pyxel.load("recursos.pyxres")

        # ---------------- ESTADO GENERAL ----------------
        self.estado = "menu"        # "menu", "config", "juego"
        self.game_over = False

        # ---------------- CONFIGURACIÓN -----------------
        # 4 velocidades posibles para el paquete
        self.velocidades = [1.5, 2.0, 2.5, 3.0]
        self.velocidades_texto = ["Muy lenta", "Lenta", "Media", "Rápida"]
        self.config_vel_index = 2  # por defecto "Media"

        # 1 o 2 paquetes
        self.config_paquetes_index = 0  # 0 => 1 paquete, 1 => 2 paquetes
        self.num_paquetes = 1

        # ---------------- MENÚ / CONFIG CURSORES --------
        self.menu_opcion = 0       # 0 = JUGAR, 1 = SALIR
        self.config_cursor = 0     # 0=velocidad,1=paquetes,2=EMPEZAR,3=VOLVER

        # ---------------- MARCADORES --------------------
        self.puntuacion = 0
        self.fallos = 0

        # ---------------- EFECTOS JEFE ------------------
        self.jefe_timer = 0        # frames que el jefe estará activo
        self.jefe_duracion = 120   # ~2 segundos
        self.shake = 0             # intensidad del temblor

        # ---------------- OBJETOS DEL JUEGO -------------
        self.camion = Camion(1 * 8, 8 * 8)
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)
        self.jefe = Jefe(15 * 8, 3 * 8)
        self.jefe.desaparecer()

        # Alturas de los tres pisos (en píxeles)
        self.pisos = [13 * 8, 8 * 8, 4 * 8]
        self.mario.pisos = self.pisos
        self.luigi.pisos = self.pisos

        # Lista de paquetes (1 o 2 según configuración)
        self.paquetes = []
        # Los paquetes se crean al iniciar partida desde la config

    # ==================================================
    #   UPDATE GENERAL (según estado)
    # ==================================================

    def update(self):
        """Actualiza el estado según el modo actual (menú, config o juego)."""
        # Salir del programa con ESC en cualquier estado
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

    # ==================================================
    #   UPDATE DEL MENÚ PRINCIPAL
    # ==================================================

    def _update_menu(self):
        """Lógica del menú principal: seleccionar JUGAR o SALIR."""
        # Mover cursor entre opciones
        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_opcion = (self.menu_opcion - 1) % 2
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_opcion = (self.menu_opcion + 1) % 2

        # Seleccionar opción con ENTER
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_opcion == 0:   # JUGAR
                self.estado = "config"
            elif self.menu_opcion == 1:  # SALIR
                pyxel.quit()

    # ==================================================
    #   UPDATE DE LA PANTALLA DE CONFIGURACIÓN
    # ==================================================

    def _update_config(self):
        """Permite elegir velocidad, nº de paquetes y empezar o volver."""
        # Mover cursor vertical
        if pyxel.btnp(pyxel.KEY_UP):
            self.config_cursor = (self.config_cursor - 1) % 4
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.config_cursor = (self.config_cursor + 1) % 4

        # Modificar opciones con izquierda/derecha
        if self.config_cursor == 0:  # Velocidad
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.config_vel_index = (self.config_vel_index - 1) % len(self.velocidades)
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_vel_index = (self.config_vel_index + 1) % len(self.velocidades)

        elif self.config_cursor == 1:  # Nº de paquetes
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_paquetes_index = 1 - self.config_paquetes_index  # alternar 0/1

        # ENTER sobre EMPEZAR o VOLVER
        if pyxel.btnp(pyxel.KEY_RETURN):
            # EMPEZAR PARTIDA
            if self.config_cursor == 2:
                self.iniciar_partida()
            # VOLVER AL MENÚ
            elif self.config_cursor == 3:
                self.estado = "menu"

    # ==================================================
    #   INICIO / REINICIO DE PARTIDA
    # ==================================================

    def iniciar_partida(self):
        """
        Aplica la configuración elegida (velocidad, nº de paquetes) y
        prepara todo para empezar una nueva partida.
        """
        # Marcadores
        self.puntuacion = 0
        self.fallos = 0
        self.game_over = False

        # Camión
        self.camion.carga = 0
        self.camion.estado = Camion.PARADO
        self.camion.x = 1 * 8
        self.camion.y = 8 * 8
        self.camion.reparto_terminado = False

        # Personajes
        self.mario.piso = 0
        self.luigi.piso = 0
        self.mario.y = self.pisos[0]
        self.luigi.y = self.pisos[0]

        # Jefe
        self.jefe.desaparecer()
        self.jefe_timer = 0
        self.shake = 0

        # Aplicar VELOCIDAD al Paquete (clase)
        Paquete.VX = self.velocidades[self.config_vel_index]

        # Nº de paquetes
        self.num_paquetes = 1 if self.config_paquetes_index == 0 else 2

        # Crear paquetes según configuración
        self._crear_paquetes_segun_config()

        # Entramos en modo juego
        self.estado = "juego"

    def _crear_paquetes_segun_config(self):
        """Crea 1 o 2 paquetes según la configuración."""
        self.paquetes = []

        # Paquete principal
        p1 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
        p1.reiniciar_salida()
        self.paquetes.append(p1)

        if self.num_paquetes == 2:
            # Segundo paquete: mismo recorrido, pero se activará más tarde.
            p2 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
            p2.reiniciar_salida()
            p2.activo = False      # no se mueve hasta que lo activemos
            self.paquetes.append(p2)

    # ==================================================
    #   UPDATE DEL JUEGO (PARTIDA)
    # ==================================================

    def _update_juego(self):
        """
        Lógica principal durante la partida.
        Gestiona:
        - Game over
        - Jefe
        - Camión
        - Personajes
        - Paquetes
        """
        # GAME OVER: sólo se puede reiniciar con R (manteniendo configuración)
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.iniciar_partida()
            return

        # Si el jefe está activo, pausamos casi todo
        if self._update_jefe_activo():
            return

        # Actualizar camión (repartos)
        if self._update_camion():
            return  # si el camión está fuera, se pausa el juego

        # Actualizar personajes (controles)
        self._update_personajes()

        # Actualizar paquetes (recorridos, fallos, puntos…)
        self._update_paquetes()

        # Comprobar si se ha llegado a 3 fallos
        if self.fallos >= 3:
            self.game_over = True

    # ---------------- UPDATE PAQUETES ------------------

    def _update_paquetes(self):
        """
        Actualiza el movimiento de los paquetes.
        Modo 2 paquetes:
        - El 2º se activa cuando el 1º ya va por piso 2 y ha pasado
          la columna morada → se aseguran recorridos bastante separados.
        """
        if self.num_paquetes == 2 and len(self.paquetes) > 1:
            p1 = self.paquetes[0]
            p2 = self.paquetes[1]

            # Activar segundo paquete cuando p1 ya está arriba (piso 2)
            # y ha pasado la columna (x <= columna morada)
            if (not p2.activo and
                    p1.piso == 2 and
                    p1.x <= Paquete.COL_COL_CONTACTO_DER * 8):
                p2.reiniciar_salida()
                p2.activo = True

        # Actualizar todos los paquetes activos
        for p in self.paquetes:
            p.update(self.mario, self.luigi, self)

    # ---------------- UPDATE JEFE ACTIVO --------------

    def _update_jefe_activo(self) -> bool:
        """
        Lógica mientras el jefe está visible tras un fallo.

        - El jefe se anima.
        - Solo se actualizan los paquetes que estén en 'caida_fallo'.
        - El resto de lógica del juego se pausa.
        Devuelve True si debe detenerse el resto del update.
        """
        if self.jefe_timer <= 0:
            return False

        # Reducir temporizador
        self.jefe_timer -= 1

        # Animar jefe
        self.jefe.update()

        # Solo dejamos caer los paquetes que están en caida_fallo
        for p in self.paquetes:
            if p.estado == "caida_fallo":
                p.update(self.mario, self.luigi, self)

        # Temblor
        self.shake = 3

        # Si se termina el tiempo, el jefe desaparece
        if self.jefe_timer <= 0:
            self.jefe.desaparecer()
            self.shake = 0

            # Cualquier paquete que haya quedado inactivo se reinicia
            for p in self.paquetes:
                if not p.activo:
                    p.reiniciar_salida()
                    p.activo = True

        # Mientras haya jefe, se pausa el resto
        return True

    # ---------------- UPDATE CAMIÓN -------------------

    def _update_camion(self) -> bool:
        """
        Actualiza el estado del camión:
        - Movimiento de salida y vuelta.
        - Reinicio de paquetes tras el reparto.
        Devuelve True si el juego debe quedar en pausa
        (cuando el camión está fuera del almacén).
        """
        self.camion.update()

        if self.camion.reparto_terminado:
            self.camion.reparto_terminado = False
            # Al terminar un reparto empezamos un "ciclo nuevo":
            # se recrean los paquetes según la configuración,
            # con el 2º desactivado si procede (para mantener separación).
            self._crear_paquetes_segun_config()

        # Mientras el camión está fuera, se pausa el juego
        if self.camion.estado == Camion.FUERA:
            return True

        return False

    # ---------------- UPDATE PERSONAJES ----------------

    def _update_personajes(self):
        """Lee el teclado y mueve a Mario y Luigi entre los pisos."""
        # Mario con flechas
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover_abajo()

        # Luigi con W / S
        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover_abajo()

    # ==================================================
    #   DRAW GENERAL (según estado)
    # ==================================================

    def draw(self):
        """Dibuja pantalla según el estado actual."""
        if self.estado == "menu":
            self._draw_menu()
        elif self.estado == "config":
            self._draw_config()
        elif self.estado == "juego":
            self._draw_juego()

    # ---------------- DIBUJO: MENÚ --------------------

    def _draw_menu(self):
        pyxel.cls(0)

        titulo = "PROYECTO SUPER MARIO"
        x_titulo = (pyxel.width - len(titulo) * 4) // 2
        pyxel.text(x_titulo, 20, titulo, 10)

        opciones = ["JUGAR", "SALIR"]
        y = 70

        for i, texto in enumerate(opciones):
            color = 7
            prefijo = "  "
            if i == self.menu_opcion:
                color = 10
                prefijo = "> "
            # 2 columnas simétricas
            if i == 0:
                x = pyxel.width // 2 - 60
            else:
                x = pyxel.width // 2 + 20
            pyxel.text(x, y, prefijo + texto, color)

    # ---------------- DIBUJO: CONFIG ------------------

    def _draw_config(self):
        pyxel.cls(0)

        titulo = "CONFIGURACION"
        x_titulo = (pyxel.width - len(titulo) * 4) // 2
        pyxel.text(x_titulo, 20, titulo, 11)

        vel_texto = self.velocidades_texto[self.config_vel_index]
        num_paquetes = "1" if self.config_paquetes_index == 0 else "2"

        lineas = [
            f"Velocidad: {vel_texto}",
            f"Paquetes: {num_paquetes}",
            "EMPEZAR PARTIDA",
            "VOLVER AL MENU"
        ]

        y = 50
        for i, texto in enumerate(lineas):
            color = 7
            prefijo = "  "
            if i == self.config_cursor:
                color = 10
                prefijo = "> "
            x = 40
            pyxel.text(x, y + i * 10, prefijo + texto, color)

    # ---------------- DIBUJO: JUEGO -------------------

    def _draw_juego(self):
        pyxel.cls(7)

        # Temblor de pantalla mientras jefe está activo
        dx = dy = 0
        if self.jefe_timer > 0:
            dx = pyxel.rndi(-self.shake, self.shake)
            dy = pyxel.rndi(-self.shake, self.shake)

        # Tilemap de fondo
        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height
        pyxel.bltm(dx, dy, 0, 0, 0, ancho, alto, colkey=7)

        # Marcadores
        pyxel.text(200, 2, f"Puntos: {self.puntuacion}", 1)
        pyxel.text(200, 10, f"Fallos: {self.fallos}", 8)
        pyxel.text(200, 18, f"Camion: {self.camion.carga}/8", 1)

        # Cruces de fallos
        self.dibujar_cruces_fallos()

        # Dibujar camión
        self.camion.draw()

        # Personajes (con temblor)
        pyxel.blt(self.luigi.x + dx, self.luigi.y + dy, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x + dx, self.mario.y + dy, *self.mario.sprite_mario)

        # Paquetes
        for p in self.paquetes:
            p.draw()

        # Jefe
        self.jefe.draw()

        # Mensaje de reparto centrado
        if self.camion.estado == Camion.FUERA:
            msg = "EL CAMION ESTA EN REPARTO..."
            x = (pyxel.width - len(msg) * 4) // 2
            y = pyxel.height // 2 - 4
            pyxel.text(x, y, msg, 8)

        # Capa de GAME OVER
        if self.game_over:
            self._draw_game_over()

    # ==================================================
    #   DIBUJO AUXILIAR (FALLOS / GAME OVER)
    # ==================================================

    def dibujar_cruces_fallos(self):
        """Dibuja las X encima de las cabezas según los fallos."""
        posiciones_x = [17 * 8, 19 * 8, 21 * 8]
        for i in range(min(self.fallos, 3)):
            pyxel.text(posiciones_x[i], 0, "X", 8)

    def _draw_game_over(self):
        """Dibuja la ventana de fin de juego sobre la pantalla, centrada."""
        # Fondo oscuro
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)

        # Panel centrado
        panel_w = 160
        panel_h = 60
        panel_x = (pyxel.width - panel_w) // 2
        panel_y = (pyxel.height - panel_h) // 2

        pyxel.rect(panel_x - 2, panel_y - 2, panel_w + 4, panel_h + 4, 8)
        pyxel.rect(panel_x, panel_y, panel_w, panel_h, 0)

        # GAME OVER centrado dentro del panel
        texto = "GAME OVER"
        x_texto = panel_x + (panel_w - len(texto) * 4) // 2
        y_texto = panel_y + 15
        pyxel.text(x_texto, y_texto, texto, pyxel.frame_count % 16)

        subt = "Pulsa R para reiniciar"
        x_sub = panel_x + (panel_w - len(subt) * 4) // 2
        y_sub = panel_y + 35
        pyxel.text(x_sub, y_sub, subt, 7)

    # ==================================================
    #   EVENTOS ESPECIALES
    # ==================================================

    def invocar_jefe(self):
        """
        Hace aparecer al jefe durante un tiempo limitado
        cuando se produce un fallo grave (paquete al vacío).
        """
        self.jefe.aparecer()
        self.jefe_timer = self.jefe_duracion
        self.shake = 3
