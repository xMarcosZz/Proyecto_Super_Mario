import pyxel


class Camion:
    """
    Representa el camión encargado de recoger paquetes.
    Su comportamiento es el siguiente:

    - Cuando recibe 8 paquetes, inicia un reparto.
    - Se mueve hacia la izquierda hasta salir de pantalla.
    - Permanece fuera unos segundos.
    - Regresa a su posición original.
    - Cuando vuelve, notifica al juego que el reparto terminó.
    """

    # Velocidad horizontal (px/frame)
    VELOCIDAD = 1

    # Posibles estados del camión
    PARADO = "parado"
    SALIENDO = "saliendo"
    FUERA = "fuera"
    VOLVIENDO = "volviendo"

    def __init__(self, x: int, y: int):
        """
        Parámetros:
            x, y — coordenadas iniciales del camión en píxeles.
        """
        self.x = x
        self.y = y
        self.x_inicial = x  # Guarda su posición original para regresar

        # Sprite del camión (img, u, v, w, h, colkey)
        self.sprite_camion = (0, 16, 32, 24, 16, 7)

        # Contador de paquetes entregados (0 a 8)
        self.carga = 0

        # Estado inicial
        self.estado = Camion.PARADO

        # Para medir el tiempo que pasa fuera
        self.timer = 0

        # Señal al juego para indicar que puede reiniciar los paquetes
        self.reparto_terminado = False

    # ============================================================
    #   CONTROL DEL CICLO DE REPARTO
    # ============================================================

    def iniciar_reparto(self):
        """
        Se llama cuando el camión llega a 8 paquetes.
        Inicia su animación de salida hacia la izquierda.
        """
        self.estado = Camion.SALIENDO
        self.reparto_terminado = False
        self.timer = 0

    def update(self):
        """
        Actualiza el estado del camión según su animación
        y el tiempo transcurrido.
        """

        # ─────────────────────────────────────────────
        # ESTADO: Saliendo del almacén hacia la izquierda
        # ─────────────────────────────────────────────
        if self.estado == Camion.SALIENDO:
            self.x -= self.VELOCIDAD

            # Cuando el camión desaparece completamente por la izquierda:
            if self.x < -40:
                self.estado = Camion.FUERA
                self.timer = pyxel.frame_count  # Guardamos instante de salida

        # ─────────────────────────────────────────────
        # ESTADO: Fuera del almacén (descanso)
        # ─────────────────────────────────────────────
        elif self.estado == Camion.FUERA:
            tiempo_fuera = pyxel.frame_count - self.timer

            # Permanece 5 segundos fuera antes de volver
            if tiempo_fuera >= 5 * 30:  # 30 FPS → 150 frames
                self.estado = Camion.VOLVIENDO
                self.x = -40  # Reaparece desde el borde izquierdo

        # ─────────────────────────────────────────────
        # ESTADO: Volviendo a su posición inicial
        # ─────────────────────────────────────────────
        elif self.estado == Camion.VOLVIENDO:
            self.x += self.VELOCIDAD

            # Si ya alcanzó su posición original
            if self.x >= self.x_inicial:
                self.x = self.x_inicial
                self.estado = Camion.PARADO
                self.carga = 0                # Reinicia la carga
                self.reparto_terminado = True  # Avisamos al juego

        # En estado PARADO no hay movimiento

    # ============================================================
    #   DIBUJADO
    # ============================================================

    def draw(self):
        """Dibuja el camión en pantalla según su sprite actual."""
        pyxel.blt(self.x, self.y, *self.sprite_camion)
