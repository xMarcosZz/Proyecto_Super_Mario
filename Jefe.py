class Jefe:
    """
    Representa al jefe que lanza los paquetes desde la parte superior.
    En el Sprint 2 solo se muestra en pantalla.
    """

    def __init__(self, x: int, y: int):
        self.x = x  # Usa el setter con validación
        self.y = y
        self.visible = True
        self.sprite_jefe = (0, 40, 32, -16, 16, 7)


    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("La coordenada X debe ser un número entero, se recibió " + str(type(x)))
        elif x < 0:
            raise ValueError("La coordenada X debe ser un número no negativo")
        else:
            self.__x = x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("La coordenada Y debe ser un número entero, se recibió " + str(type(y)))
        elif y < 0:
            raise ValueError("La coordenada Y debe ser un número no negativo")
        else:
            self.__y = y

    # --------- VISIBILIDAD ---------
    def aparecer(self):
        self.visible = True

    def desaparecer(self):
        self.visible = False

    def update(self):
        pass


