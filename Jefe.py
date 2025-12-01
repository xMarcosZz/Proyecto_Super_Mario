import pyxel

class Jefe:
    """
    Jefe que aparece en la columna central y tiene una pequeña animación simple
    alternando entre dos poses.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        # Por defecto oculto
        self.visible = False

        # ──────────────────────────────────────────────
        #   SPRITES DEL JEFE
        # ──────────────────────────────────────────────
        self.sprite_pose_1 = (0, 40, 32, -16, 16, 7)   # Jefe pose 1
        self.sprite_pose_2 = (0, 56, 32,  16, 16, 7)   # Jefe pose 2

        # La pose actual comienza siendo la primera
        self.sprite_actual = self.sprite_pose_1

        # ──────────────────────────────────────────────
        #   VARIABLES DE ANIMACIÓN
        # ──────────────────────────────────────────────
        self.frame_index = 0
        self.anim_contador = 0
        self.anim_velocidad = 5  # cambia cada 10 frames

    # ---------------------------------------------
    # Propiedades X/Y (para mantener tu estilo)
    # ---------------------------------------------
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

    # ---------------------------------------------
    # Control de visibilidad
    # ---------------------------------------------
    def aparecer(self):
        self.visible = True

    def desaparecer(self):
        self.visible = False

    # ---------------------------------------------
    # Lógica de animación
    # ---------------------------------------------
    def update(self):
        if not self.visible:
            return

        self.anim_contador += 1

        if self.anim_contador >= self.anim_velocidad:
            self.anim_contador = 0

            # Alternar entre pose 1 y pose 2
            if self.sprite_actual == self.sprite_pose_1:
                self.sprite_actual = self.sprite_pose_2
            else:
                self.sprite_actual = self.sprite_pose_1

    # ---------------------------------------------
    # Dibujado
    # ---------------------------------------------
    def draw(self):
        if not self.visible:
            return

        img, u, v, w, h, colkey = self.sprite_actual
        pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)
