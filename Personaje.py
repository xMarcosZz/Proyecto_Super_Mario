import pyxel


class Personaje:
    """
    Representa a un personaje del juego (Mario o Luigi).
    Se encarga de almacenar su posición, sprite, piso actual y
    permite moverlo verticalmente entre los pisos definidos por el juego.
    """

    def __init__(self, nombre: str, x: int, y: int):
        """
        Inicializa un personaje con nombre, posición y sprite.
        Parámetros:
            nombre: "Mario" o "Luigi"
            x, y : posición inicial en píxeles
        """
        self.nombre = nombre

        # Usan setters → validación
        self.x = x
        self.y = y

        # Sprites de ambos personajes (img, u, v, w, h, colkey)
        self.sprite_luigi = (0, 16, 0, 16, 16, 7)
        self.sprite_mario = (0, 0, 0, 16, 16, 7)

        # Piso actual (0 = abajo)
        self.piso = 0

        # Lista con alturas y-coord de cada piso (se asigna desde Juego)
        self.pisos = None

    # ==========================================================
    #  PROPIEDADES X / Y CON VALIDACIÓN
    # ==========================================================

    @property
    def x(self) -> int:
        """Coordenada X del personaje (en píxeles)."""
        return self.__x

    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError("La coordenada X debe ser un número entero.")
        if value < 0:
            raise ValueError("La coordenada X debe ser un número no negativo.")
        self.__x = value

    @property
    def y(self) -> int:
        """Coordenada Y del personaje (en píxeles)."""
        return self.__y

    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError("La coordenada Y debe ser un número entero.")
        if value < 0:
            raise ValueError("La coordenada Y debe ser un número no negativo.")
        self.__y = value

    # ==========================================================
    #  MOVIMIENTO ENTRE PISOS
    # ==========================================================

    def mover_arriba(self):
        """
        Mueve al personaje un piso hacia arriba si no está en el piso superior.
        """
        if self.pisos is None:
            raise ValueError("Los pisos no han sido asignados al personaje.")

        if self.piso < len(self.pisos) - 1:
            self.piso += 1
            self.y = self.pisos[self.piso]

    def mover_abajo(self):
        """
        Mueve al personaje un piso hacia abajo si no está en el inferior.
        """
        if self.pisos is None:
            raise ValueError("Los pisos no han sido asignados al personaje.")

        if self.piso > 0:
            self.piso -= 1
            self.y = self.pisos[self.piso]

    # ==========================================================
    #  DIBUJADO DEL PERSONAJE
    # ==========================================================

    def draw(self):
        """
        Dibuja el sprite correspondiente de Mario o Luigi.
        Este método se usa desde Juego.draw().
        """
        if self.nombre.lower() == "luigi":
            pyxel.blt(self.x, self.y, *self.sprite_luigi)
        else:
            pyxel.blt(self.x, self.y, *self.sprite_mario)
