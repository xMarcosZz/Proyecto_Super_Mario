import pyxel


class Camion:
    """
    Representa el camión encargado de recoger paquetes.
    Cuando acumula 8 paquetes, sale a reparto, desaparece unos segundos
    y después regresa a su posición original.
    """

    VELOCIDAD = 1  # Velocidad horizontal del camión (px/frame)

    # Estados posibles:
    PARADO = "parado"
    SALIENDO = "saliendo"
    FUERA = "fuera"
    VOLVIENDO = "volviendo"

    def __init__(self, x: int, y: int):
        """
        Parámetros:
            x, y — Coordenadas iniciales del camión
        """
        self.x = x
        self.y = y
        self.x_inicial = x  # Guarda su posición base para volver

        # Sprite del camión (img, u, v, w, h, colkey)
        self.sprite_camion = (0, 16, 32, 24, 16, 7)

        # Cantidad de paquetes entregados (0 a 8)
        self.carga = 0

        # Estado inicial
        self.estado = Camion.PARADO

        # Timer para controlar cuánto tiempo está fuera
        self.timer = 0

        # Indica si el camión ha terminado el reparto (para que el juego respawnee un paquete)
        self.reparto_terminado = False

    # -------------------------------------------------------------------
    #   LÓGICA DEL REPARTO
    # -------------------------------------------------------------------

    def iniciar_reparto(self):
        """
        Llamado cuando el camión alcanza 8 paquetes entregados.
        Inicia la animación de salida hacia la izquierda.
        """
        self.estado = Camion.SALIENDO
        self.reparto_terminado = False
        self.timer = 0

    def update(self):
        """Actualiza la posición y el estado del camión según su animación."""

        # ───────────────────────────────────────────
        # ESTADO: saliendo hacia la izquierda
        # ───────────────────────────────────────────
        if self.estado == Camion.SALIENDO:
            self.x -= self.VELOCIDAD

            # ¿Está ya completamente fuera de la pantalla?
            if self.x < -40:
                self.estado = Camion.FUERA
                self.timer = pyxel.frame_count  # Guarda el instante en el que salió

        # ───────────────────────────────────────────
        # ESTADO: fuera (descanso de 5 segundos)
        # ───────────────────────────────────────────
        elif self.estado == Camion.FUERA:
            tiempo_fuera = pyxel.frame_count - self.timer

            if tiempo_fuera > 5 * 30:  # 5 segundos a 30 FPS
                self.estado = Camion.VOLVIENDO
                self.x = -40  # Reaparece desde la izquierda

        # ───────────────────────────────────────────
        # ESTADO: volviendo hacia la posición inicial
        # ───────────────────────────────────────────
        elif self.estado == Camion.VOLVIENDO:
            self.x += self.VELOCIDAD

            if self.x >= self.x_inicial:
                self.x = self.x_inicial
                self.estado = Camion.PARADO
                self.carga = 0            # Reiniciar carga
                self.reparto_terminado = True  # Avisar al juego

        # Si está PARADO, no hace nada especial

    # -------------------------------------------------------------------
    #   DIBUJADO
    # -------------------------------------------------------------------

    def draw(self):
        """Dibuja el camión en pantalla según su sprite."""
        pyxel.blt(self.x, self.y, *self.sprite_camion)
