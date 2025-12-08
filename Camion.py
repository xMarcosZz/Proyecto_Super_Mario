import pyxel


class Camion:
    """
    Representa el camión encargado de recoger paquetes.
    Gestiona la carga de paquetes y la animación de salir a reparto.
    """

    # Definimos constantes para los estados
    PARADO = "parado"
    SALIENDO = "saliendo"
    FUERA = "fuera"
    VOLVIENDO = "volviendo"

    # Velocidad a la que se mueve el camión
    VELOCIDAD = 1

    #Setters\Getters
    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int):
        self.__x = int(value)

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int):
        self.__y = int(value)

    def __init__(self, x: int, y: int):
        """Constructor del camión."""
        self.x = x
        self.y = y
        self.x_inicial = x  # Guardamos la X original para saber dónde volver

        # Sprite del camión (img, u, v, w, h, colkey)
        self.sprite_camion = (0, 16, 32, 24, 16, 7)

        # Carga actual (máximo 8)
        self.carga = 0

        # Estado inicial
        self.estado = Camion.PARADO

        # Timer para controlar el tiempo de espera fuera
        self.timer = 0

        # Bandera para avisar al juego de que ha terminado el reparto
        self.reparto_terminado = False

    def iniciar_reparto(self):
        """
        Cambia el estado para que el camión empiece a moverse.
        Se llama cuando la carga llega a 8.
        """
        self.estado = Camion.SALIENDO
        self.reparto_terminado = False
        self.timer = 0

    def update(self):
        """
        Máquina de estados del camión.
        Controla el movimiento y el tiempo según el estado actual.
        """

        # CASO 1: El camión está saliendo hacia la izquierda
        if self.estado == Camion.SALIENDO:
            self.x = self.x - self.VELOCIDAD

            # Si el camión se ha ido completamente de la pantalla
            if self.x < -40:
                self.estado = Camion.FUERA
                # Guardamos el frame actual para contar el tiempo
                self.timer = pyxel.frame_count

        # CASO 2: El camión está fuera (Reparto)
        elif self.estado == Camion.FUERA:
            # Calculamos cuánto tiempo ha pasado
            tiempo_fuera = pyxel.frame_count - self.timer
            duracion_espera = 5 * 30  # 5 segundos * 30 FPS

            if tiempo_fuera >= duracion_espera:
                self.estado = Camion.VOLVIENDO
                # Colocamos el camión justo fuera de la pantalla para que entre
                self.x = -40

        # CASO 3: El camión está volviendo al sitio
        elif self.estado == Camion.VOLVIENDO:
            self.x = self.x + self.VELOCIDAD

            # Si ha llegado a su posición original
            if self.x >= self.x_inicial:
                self.x = self.x_inicial
                self.estado = Camion.PARADO
                self.carga = 0                # Vaciamos la carga
                self.reparto_terminado = True  # Avisamos al juego

        # CASO 4: PARADO
        # No hacemos nada si está parado

    def draw(self):
        """Dibuja el camión."""
        pyxel.blt(self.x, self.y, *self.sprite_camion)