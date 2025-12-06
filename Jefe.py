import pyxel


class Jefe:
    """
    Representa al jefe que aparece cuando el jugador comete un fallo.
    Aparece en una posición fija y tiene una animación simple.
    """

    def __init__(self, x: int, y: int):
        """
        Constructor del Jefe.
        """
        self.x = x
        self.y = y

        # Variable para controlar si se dibuja o no
        self.visible = False

        # Lista de sprites para la animación (dos poses distintas)
        self.sprites = [
            (0, 40, 32, -16, 16, 7),  # Pose 1
            (0, 56, 32, 16, 16, 7),  # Pose 2
        ]

        # Índice para saber qué sprite dibujar (0 o 1)
        self.frame_index = 0

        # Variables para controlar la velocidad de la animación
        self.anim_contador = 0
        self.anim_velocidad = 5  # Cambia de pose cada 5 frames

    # --------------------------------------------------
    # PROPIEDADES (Getters y Setters)
    # --------------------------------------------------
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

    # --------------------------------------------------
    # VISIBILIDAD
    # --------------------------------------------------
    def aparecer(self):
        """Hace visible al jefe para regañar."""
        self.visible = True

    def desaparecer(self):
        """Oculta al jefe y reinicia su animación."""
        self.visible = False
        self.frame_index = 0

    # --------------------------------------------------
    # ACTUALIZACIÓN (Update)
    # --------------------------------------------------
    def update(self):
        """
        Controla la animación del jefe.
        """
        # Si no está visible, no necesitamos actualizar nada
        if self.visible == False:
            return

        # Incrementamos el contador de tiempo
        self.anim_contador = self.anim_contador + 1

        # Si el contador llega al límite, cambiamos de pose
        if self.anim_contador >= self.anim_velocidad:
            self.anim_contador = 0

            # Alternamos el índice entre 0 y 1
            if self.frame_index == 0:
                self.frame_index = 1
            else:
                self.frame_index = 0

    # --------------------------------------------------
    # DIBUJADO (Draw)
    # --------------------------------------------------
    def draw(self):
        """Dibuja al jefe en pantalla."""
        if self.visible == False:
            return

        # Obtenemos los datos del sprite actual
        sprite_actual = self.sprites[self.frame_index]

        # Desempaquetamos los valores para pasarlos a blt
        img, u, v, w, h, colkey = sprite_actual

        pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)