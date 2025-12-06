import pyxel
import time  # Importamos la librería 'time' para leer la hora del ordenador


class HUD:
    """
    Clase HUD (Heads-Up Display)
    ----------------------------
    Se encarga exclusivamente de PINTAR la interfaz de usuario.
    Ahora incluye métodos para:
    1. Dibujar un reloj en tiempo real.
    2. Dibujar una ventana de pausa superpuesta.
    """

    # =========================================================================
    # MENÚ PRINCIPAL
    # =========================================================================
    def draw_menu(self, opcion_seleccionada):
        """Dibuja la pantalla del menú principal."""
        pyxel.cls(0)

        # Título
        titulo = "PROYECTO SUPER MARIO"
        x_tit = (pyxel.width - len(titulo) * 4) // 2
        pyxel.text(x_tit, 30, titulo, 10)

        opciones = ["JUGAR", "SALIR"]
        y_inicial = 70

        for i, txt in enumerate(opciones):
            es_sel = (i == opcion_seleccionada)

            if es_sel:
                prefix = "> "
                suffix = " <"
                color = 7
            else:
                prefix = "  "
                suffix = "  "
                color = 13

            texto_completo = prefix + txt + suffix
            x_txt = (pyxel.width - len(texto_completo) * 4) // 2
            pyxel.text(x_txt, y_inicial + i * 15, texto_completo, color)

        # --- NUEVO: DIBUJAMOS LA HORA ---
        self.draw_reloj()

    # =========================================================================
    # CONFIGURACIÓN
    # =========================================================================
    def draw_config(self, cursor, vel_texto, num_paquetes):
        """Dibuja la pantalla de configuración."""
        pyxel.cls(0)
        t = "CONFIGURACION"
        pyxel.text((pyxel.width - len(t) * 4) // 2, 20, t, 11)

        if num_paquetes == 1:
            np_txt = "1"
        else:
            np_txt = "2"

        items = [
            f"Velocidad: {vel_texto}",
            f"Paquetes: {np_txt}",
            "EMPEZAR PARTIDA",
            "VOLVER AL MENU"
        ]

        y = 50
        for i, txt in enumerate(items):
            if i == cursor:
                color = 10
                prefix = "> "
            else:
                color = 7
                prefix = "  "
            pyxel.text(40, y + i * 10, prefix + txt, color)

        # --- NUEVO: DIBUJAMOS LA HORA ---
        self.draw_reloj()

    # =========================================================================
    # INTERFAZ DE JUEGO (Marcadores)
    # =========================================================================
    def draw_marcador_juego(self, puntuacion, record, fallos, carga_camion):
        """Dibuja el panel lateral derecho con las estadísticas."""
        hud_x = 190
        hud_y = 2
        hud_w = 60
        hud_h = 45

        # Caja del marcador
        pyxel.rect(hud_x, hud_y, hud_w, hud_h, 0)
        pyxel.rectb(hud_x, hud_y, hud_w, hud_h, 13)

        # Puntuación
        pyxel.text(hud_x + 4, hud_y + 4, "SCORE", 6)
        pyxel.text(hud_x + 35, hud_y + 4, str(puntuacion), 7)

        # Récord
        pyxel.text(hud_x + 4, hud_y + 14, "HIGH", 6)
        pyxel.text(hud_x + 35, hud_y + 14, str(record), 10)

        # Fallos
        pyxel.text(hud_x + 4, hud_y + 24, "MISS", 6)
        for i in range(3):
            if i < fallos:
                col = 8
                txt = "X"
            else:
                col = 1
                txt = "-"
            pyxel.text(hud_x + 35 + (i * 6), hud_y + 24, txt, col)

        # Carga del camión
        pyxel.text(hud_x + 4, hud_y + 34, "LOAD", 6)
        pyxel.rect(hud_x + 28, hud_y + 35, 24, 4, 1)
        ancho = int((carga_camion / 8) * 24)
        pyxel.rect(hud_x + 28, hud_y + 35, ancho, 4, 11)

        # --- NUEVO: DIBUJAMOS LA HORA DENTRO DEL JUEGO ---
        self.draw_reloj()

    # =========================================================================
    # NUEVO: RELOJ Y PAUSA
    # =========================================================================

    def draw_reloj(self):
        """
        Dibuja la hora actual del sistema en la esquina superior izquierda.
        Útil para que el jugador no pierda la noción del tiempo.
        """
        # Obtenemos la hora actual en formato HH:MM (Ej: "18:45")
        hora_actual = time.strftime("%H:%M")

        # Dibujamos un pequeño rectángulo negro detrás para que se lea
        # aunque el fondo del juego sea de otro color
        pyxel.rect(2, 2, 25, 7, 0)

        # Escribimos la hora en blanco
        pyxel.text(4, 3, hora_actual, 7)

    def draw_pausa(self, cursor_pausa, puntuacion_actual):
        """
        Dibuja una ventana flotante sobre el juego cuando está en PAUSA.
        (Sin efecto de oscurecimiento de fondo)
        """

        # 1. CAJA DEL MENÚ (Ventana central)
        ancho = 100
        alto = 60

        # Calculamos coordenadas para centrar la caja
        x_caja = (pyxel.width - ancho) // 2
        y_caja = (pyxel.height - alto) // 2

        # Dibujamos fondo negro y borde blanco PARA LA CAJA
        pyxel.rect(x_caja, y_caja, ancho, alto, 0)
        pyxel.rectb(x_caja, y_caja, ancho, alto, 7)

        # 2. CONTENIDO DE LA PAUSA

        # Título centrado
        titulo = "- PAUSA -"
        x_tit = x_caja + (ancho - len(titulo) * 4) // 2
        pyxel.text(x_tit, y_caja + 8, titulo, 10)  # Amarillo

        # Mostramos la puntuación actual
        texto_puntos = f"Puntos: {puntuacion_actual}"
        x_pts = x_caja + (ancho - len(texto_puntos) * 4) // 2
        pyxel.text(x_pts, y_caja + 20, texto_puntos, 6)  # Gris claro

        # Opciones del menú de pausa
        opciones = ["CONTINUAR", "SALIR AL MENU"]
        y_opciones = y_caja + 35

        for i, txt in enumerate(opciones):
            if i == cursor_pausa:
                color = 10  # Amarillo
                prefix = "> "
            else:
                color = 7  # Blanco
                prefix = "  "

            pyxel.text(x_caja + 20, y_opciones + i * 10, prefix + txt, color)

    # =========================================================================
    # OTROS MENSAJES
    # =========================================================================

    def draw_mensaje_descanso(self):
        msg = "DESCANSO..."
        cx = pyxel.width // 2
        cy = pyxel.height // 2
        pyxel.text(cx - len(msg) * 2, cy, msg, 0)
        pyxel.text(cx - len(msg) * 2 - 1, cy - 1, msg, 8)

    def draw_game_over(self, puntuacion, record, es_nuevo_record):
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)
        cx = pyxel.width // 2
        cy = pyxel.height // 2

        t1 = "GAME OVER"
        pyxel.text(cx - len(t1) * 2, cy - 20, t1, 8)

        t2 = f"SCORE: {puntuacion}"
        pyxel.text(cx - len(t2) * 2, cy, t2, 7)

        if es_nuevo_record:
            t3 = "!NUEVO RECORD!"
            pyxel.text(cx - len(t3) * 2, cy + 10, t3, 10)

        t4 = "PULSA R"
        pyxel.text(cx - len(t4) * 2, cy + 30, t4, 6)