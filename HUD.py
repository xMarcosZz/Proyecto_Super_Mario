import pyxel
import time


class HUD:
    """
    Clase encargada de dibujar la interfaz grafica.
    Dibuja menus, puntuaciones y mensajes.
    """

    def draw_menu(self, opcion_seleccionada):
        # Limpiamos la pantalla de negro
        pyxel.cls(0)

        # Dibujamos el titulo centrado
        titulo = "PROYECTO SUPER MARIO"
        ancho_titulo = len(titulo) * 4
        x_tit = (pyxel.width - ancho_titulo) // 2
        pyxel.text(x_tit, 30, titulo, 10)

        # Lista de opciones del menu
        opciones = ["JUGAR", "SALIR"]
        y_inicial = 70

        # Recorremos las opciones para dibujarlas una a una
        for i, txt in enumerate(opciones):
            # Comprobamos si esta opcion es la seleccionada
            if i == opcion_seleccionada:
                prefix = "> "
                suffix = " <"
                color = 7
            else:
                prefix = "  "
                suffix = "  "
                color = 13

            # Construimos el texto completo
            texto_completo = prefix + txt + suffix

            # Calculamos la posicion X para centrarlo
            ancho_texto = len(texto_completo) * 4
            x_txt = (pyxel.width - ancho_texto) // 2

            # Calculamos la posicion Y
            pos_y = y_inicial + (i * 15)

            pyxel.text(x_txt, pos_y, texto_completo, color)

        # Dibujamos el reloj
        self.draw_reloj()

    def draw_config(self, cursor, vel_texto, num_paquetes):
        # Limpiamos pantalla
        pyxel.cls(0)

        # Titulo de configuracion
        t = "CONFIGURACION"
        ancho_t = len(t) * 4
        x_t = (pyxel.width - ancho_t) // 2
        pyxel.text(x_t, 20, t, 11)

        # Convertimos el numero de paquetes a texto
        if num_paquetes == 1:
            np_txt = "1"
        else:
            np_txt = "2"

        # Creamos los textos de las opciones
        texto_velocidad = "Velocidad: " + vel_texto
        texto_paquetes = "Paquetes: " + np_txt
        items = [texto_velocidad, texto_paquetes, "EMPEZAR PARTIDA", "VOLVER AL MENU"]

        y = 50

        # Dibujamos cada opcion
        for i, txt in enumerate(items):
            # Comprobamos si el cursor esta aqui
            if i == cursor:
                color = 10
                prefix = "> "
            else:
                color = 7
                prefix = "  "

            pos_y = y + (i * 10)
            pyxel.text(40, pos_y, prefix + txt, color)

        self.draw_reloj()

    def draw_marcador_juego(self, puntuacion, record, fallos, carga_camion):
        # Coordenadas del panel
        x = 190
        y = 2
        w = 60
        h = 45

        # Dibujamos la caja del marcador
        pyxel.rect(x, y, w, h, 0)
        pyxel.rectb(x, y, w, h, 13)

        # Texto Puntuacion
        pyxel.text(x + 4, y + 4, "SCORE", 6)
        pyxel.text(x + 35, y + 4, str(puntuacion), 7)

        # Texto Record
        pyxel.text(x + 4, y + 14, "HIGH", 6)
        pyxel.text(x + 35, y + 14, str(record), 10)

        # Texto Fallos
        pyxel.text(x + 4, y + 24, "MISS", 6)

        # Dibujamos las cruces de los fallos
        for i in range(3):
            if i < fallos:
                color = 8
                caracter = "X"
            else:
                color = 1
                caracter = "-"

            pos_x_cruz = x + 35 + (i * 6)
            pyxel.text(pos_x_cruz, y + 24, caracter, color)

        # Barra de carga del camion
        pyxel.text(x + 4, y + 34, "LOAD", 6)

        # Fondo de la barra
        pyxel.rect(x + 28, y + 35, 24, 4, 1)

        # Parte rellena de la barra
        # Calculamos el ancho de forma basica
        porcentaje = carga_camion / 8
        ancho_barra = int(porcentaje * 24)

        pyxel.rect(x + 28, y + 35, ancho_barra, 4, 11)

        self.draw_reloj()

    def draw_reloj(self):
        # Obtenemos la hora del sistema
        hora_actual = time.strftime("%H:%M")

        # Fondo negro para que se lea bien
        pyxel.rect(2, 2, 25, 7, 0)
        # Texto blanco
        pyxel.text(4, 3, hora_actual, 7)

    def draw_pausa(self, cursor_pausa, puntuacion_actual):
        # Dibuja la ventana de pausa

        # Dimensiones de la ventana
        ancho = 100
        alto = 60

        # Calculo para centrar la ventana
        x_caja = (pyxel.width - ancho) // 2
        y_caja = (pyxel.height - alto) // 2

        # Fondo negro
        pyxel.rect(x_caja, y_caja, ancho, alto, 0)
        # Borde blanco
        pyxel.rectb(x_caja, y_caja, ancho, alto, 7)

        # Titulo de Pausa
        titulo = "- PAUSA -"
        ancho_tit = len(titulo) * 4
        x_tit = x_caja + (ancho - ancho_tit) // 2
        pyxel.text(x_tit, y_caja + 8, titulo, 10)

        # Mostrar puntuacion
        texto_puntos = "Puntos: " + str(puntuacion_actual)
        ancho_pts = len(texto_puntos) * 4
        x_pts = x_caja + (ancho - ancho_pts) // 2
        pyxel.text(x_pts, y_caja + 20, texto_puntos, 6)

        # Opciones del menu de pausa
        opciones = ["CONTINUAR", "SALIR AL MENU"]
        y_opciones = y_caja + 35

        for i, txt in enumerate(opciones):
            if i == cursor_pausa:
                color = 10
                prefix = "> "
            else:
                color = 7
                prefix = "  "

            pos_y_opcion = y_opciones + (i * 10)
            pyxel.text(x_caja + 20, pos_y_opcion, prefix + txt, color)

    def draw_mensaje_descanso(self):
        # Mensaje cuando el camion esta fuera
        msg = "DESCANSO..."
        ancho_msg = len(msg) * 4

        cx = pyxel.width // 2
        cy = pyxel.height // 2

        x_texto = cx - (ancho_msg // 2)

        # Sombra negra
        pyxel.text(x_texto, cy, msg, 0)
        # Texto rojo principal
        pyxel.text(x_texto - 1, cy - 1, msg, 8)

    def draw_game_over(self, puntuacion, record, es_nuevo_record):
        # Pantalla de Game Over

        # Fondo negro completo
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)

        cx = pyxel.width // 2
        cy = pyxel.height // 2

        # Texto Game Over
        t1 = "GAME OVER"
        ancho_t1 = len(t1) * 4
        pyxel.text(cx - (ancho_t1 // 2), cy - 25, t1, 8)

        # Texto Puntuacion
        t2 = "SCORE: " + str(puntuacion)
        ancho_t2 = len(t2) * 4
        pyxel.text(cx - (ancho_t2 // 2), cy - 10, t2, 7)

        # Mensaje de Nuevo Record
        if es_nuevo_record:
            t3 = "!NUEVO RECORD!"
            ancho_t3 = len(t3) * 4
            pyxel.text(cx - (ancho_t3 // 2), cy, t3, 10)

        # Opciones
        t_reintentar = "R: REINTENTAR"
        ancho_tr = len(t_reintentar) * 4
        pyxel.text(cx - (ancho_tr // 2), cy + 20, t_reintentar, 6)

        t_menu = "M: MENU PRINCIPAL"
        ancho_tm = len(t_menu) * 4
        pyxel.text(cx - (ancho_tm // 2), cy + 30, t_menu, 6)