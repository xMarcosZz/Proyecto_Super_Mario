import pyxel

class Camion:

    VELOCIDAD = 1

    def __init__(self, x, y):
        # posiciones iniciales
        self.x = x
        self.y = y
        self.x_inicial = x

        # gráfico
        self.sprite_camion = (0, 16, 32, 24, 16, 7)

        # carga de paquetes
        self.carga = 0

        # estado del camión
        # "parado" → normal
        # "saliendo" → se va a la izquierda
        # "fuera" → desaparecido
        # "volviendo" → vuelve por la derecha
        self.estado = "parado"

        # para controlar tiempos
        self.timer = 0

        # importante para el respawn del paquete
        self.reparto_terminado = False

    def iniciar_reparto(self):
        """Llamado cuando carga == 8"""
        self.estado = "saliendo"
        self.reparto_terminado = False
        self.timer = 0

    def update(self):
        # ESTADO: saliendo a la izquierda
        if self.estado == "saliendo":
            self.x -= self.VELOCIDAD
            if self.x < -40:  # ya salió
                self.estado = "fuera"
                self.timer = pyxel.frame_count

        # ESTADO: fuera (pausa de 5 segundos)
        elif self.estado == "fuera":
            if pyxel.frame_count - self.timer > 5 * 30:
                self.estado = "volviendo"
                self.x = -40

        # ESTADO: volviendo por la derecha
        elif self.estado == "volviendo":
            self.x += self.VELOCIDAD
            if self.x >= self.x_inicial:
                self.x = self.x_inicial
                self.estado = "parado"
                self.carga = 0
                self.reparto_terminado = True  # avisa al juego que puede aparecer un paquete

    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite_camion)
