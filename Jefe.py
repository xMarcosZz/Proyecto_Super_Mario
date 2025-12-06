import pyxel


class Jefe:
    """
    Representa al jefe que aparece cuando el jugador comete un fallo.
    El jefe se coloca en la parte superior central y alterna entre dos poses
    para simular una animación básica.
    """

    def __init__(self, x: int, y: int):
        """
        Inicializa el jefe con su posición y sus sprites.
        Parámetros:
            x, y — coordenadas iniciales donde se dibuja el jefe.
        """
        self.x = x
        self.y = y

        # Estado de visibilidad del jefe
        self.visible = False

        # ──────────────────────────────────────────────
        # SPRITES DEL JEFE (pose 1 y pose 2)
        # (img, u, v, w, h, colkey)
        # Nota: El uso de lista + índice permite expandir a más poses fácilmente.
        # ──────────────────────────────────────────────
        self.sprites = [
            (0, 40, 32, -16, 16, 7),   # sprite_pose_1
            (0, 56, 32,  16, 16, 7),   # sprite_pose_2
        ]

        self.frame_index = 0  # índice actual de sprite

        # Variables de animación
        self.anim_contador = 0
        self.anim_velocidad = 5  # número de frames por cambio de pose

    # --------------------------------------------------
    # PROPIEDADES X/Y (para mantener estilo uniforme)
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
    # CONTROL DE VISIBILIDAD
    # --------------------------------------------------
    def aparecer(self):
        """Muestra al jefe en pantalla."""
        self.visible = True

    def desaparecer(self):
        """Oculta al jefe y reinicia la animación."""
        self.visible = False
        self.frame_index = 0

    # --------------------------------------------------
    # ANIMACIÓN
    # --------------------------------------------------
    def update(self):
        """
        Actualiza la animación alternando de sprite cada X frames.
        Si el jefe está oculto, no hace nada.
        """
        if not self.visible:
            return

        self.anim_contador += 1

        if self.anim_contador >= self.anim_velocidad:
            self.anim_contador = 0
            # Cambia entre 0 ↔ 1 (dos poses)
            self.frame_index = 1 - self.frame_index

    # --------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------
    def draw(self):
        """Dibuja al jefe si se encuentra visible."""
        if not self.visible:
            return

        img, u, v, w, h, colkey = self.sprites[self.frame_index]
        pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)
