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
        """
        self.nombre = nombre

        # Usamos los setters para validar que x e y sean correctos
        self.x = x
        self.y = y

        # Definimos los sprites (img, u, v, w, h, colkey)
        self.sprite_luigi = (0, 16, 0, 16, 16, 7)
        self.sprite_mario = (0, 0, 0, 16, 16, 7)

        # Piso actual (0 es el piso de más arriba en lógica, o abajo según se mire)
        self.piso = 0

        # Lista donde guardaremos las coordenadas Y de cada piso
        self.pisos = None

    # ==========================================================
    #  PROPIEDADES X / Y CON VALIDACIÓN
    # ==========================================================

    @property
    def x(self) -> int:
        """Devuelve la coordenada X."""
        return self.__x

    @x.setter
    def x(self, value: int):
        """Asigna la coordenada X comprobando que sea válida."""
        if not isinstance(value, int):
            raise TypeError("La coordenada X debe ser un número entero.")
        if value < 0:
            raise ValueError("La coordenada X debe ser un número no negativo.")
        self.__x = value

    @property
    def y(self) -> int:
        """Devuelve la coordenada Y."""
        return self.__y

    @y.setter
    def y(self, value: int):
        """Asigna la coordenada Y comprobando que sea válida."""
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
        Mueve al personaje un piso hacia arriba (visualmente)
        si no está ya en el límite superior.
        """
        # Comprobamos que el juego nos haya dado la lista de pisos
        if self.pisos is None:
            raise ValueError("Los pisos no han sido asignados al personaje.")

        # Verificamos si podemos subir más
        # Nota: Dependiendo de cómo ordenes la lista 'pisos', el índice cambia.
        # Aquí asumimos que índice mayor = piso superior visualmente o viceversa.
        # Ajustado a la lógica del juego: índice mayor = subir.
        if self.piso < len(self.pisos) - 1:
            self.piso = self.piso + 1
            # Actualizamos la posición visual Y
            self.y = self.pisos[self.piso]

    def mover_abajo(self):
        """
        Mueve al personaje un piso hacia abajo.
        """
        if self.pisos is None:
            raise ValueError("Los pisos no han sido asignados al personaje.")

        # Verificamos si podemos bajar más
        if self.piso > 0:
            self.piso = self.piso - 1
            # Actualizamos la posición visual Y
            self.y = self.pisos[self.piso]

    # ==========================================================
    #  DIBUJADO DEL PERSONAJE
    # ==========================================================

    def draw(self):
        """
        Dibuja el sprite correspondiente de Mario o Luigi.
        """
        # Convertimos el nombre a minúsculas para comparar
        if self.nombre.lower() == "luigi":
            pyxel.blt(self.x, self.y, *self.sprite_luigi)
        else:
            pyxel.blt(self.x, self.y, *self.sprite_mario)