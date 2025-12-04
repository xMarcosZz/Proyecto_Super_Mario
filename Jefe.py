import pyxel


class Jefe:
    """
    Representa al jefe que aparece en la columna central cuando el jugador
    comete un fallo. El jefe muestra una animación sencilla alternando dos poses.
    """

    def __init__(self, x: int, y: int):
        """
        Inicializa el jefe con su posición en pantalla y sus sprites.
        Parámetros:
            x, y — coordenadas en píxeles donde se dibujará el jefe.
        """
        self.x = x
        self.y = y

        # Por defecto, el jefe está oculto.
        self.visible = False

        # ──────────────────────────────────────────────
        #   SPRITES DEL JEFE (pose 1 y pose 2)
        #   (img, u, v, w, h, colkey)
        # ──────────────────────────────────────────────
        self.pose_1 = (0, 40, 32, -16, 16, 7)
        self.pose_2 = (0, 56, 32,  16, 16, 7)

        # Sprite actual que se dibuja
        self.sprite_actual = self.pose_1

        # ──────────────────────────────────────────────
        #   VARIABLES DE ANIMACIÓN
        # ──────────────────────────────────────────────
        self.anim_contador = 0
        self.anim_velocidad = 5  # cambia cada 5 frames

    # --------------------------------------------------
    #  PROPIEDADES X E Y (con validación básica)
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
    #  CONTROL DE VISIBILIDAD
    # --------------------------------------------------
    def aparecer(self):
        """Hace visible al jefe para que pueda dibujarse y animarse."""
        self.visible = True

    def desaparecer(self):
        """Oculta al jefe y detiene su animación."""
        self.visible = False

    # --------------------------------------------------
    #  ANIMACIÓN
    # --------------------------------------------------
    def update(self):
        """
        Actualiza la animación del jefe alternando entre dos poses
        si está visible. Si está oculto, no hace nada.
        """
        if not self.visible:
            return

        self.anim_contador += 1

        if self.anim_contador >= self.anim_velocidad:
            self.anim_contador = 0

            # Alternar entre pose 1 y pose 2
            if self.sprite_actual == self.pose_1:
                self.sprite_actual = self.pose_2
            else:
                self.sprite_actual = self.pose_1

    # --------------------------------------------------
    #  DIBUJADO
    # --------------------------------------------------
    def draw(self):
        """Dibuja al jefe si está visible."""
        if not self.visible:
            return

        img, u, v, w, h, colkey = self.sprite_actual
        pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)
