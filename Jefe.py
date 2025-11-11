class Jefe:
    def __init__(self, x: int, y: int):
        self.x = x   # Usa el setter con validación
        self.y = y
        self.visible = True

    # Propiedad y setter para X
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

    # Propiedad y setter para Y
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

    def aparecer(self):
        """Hace visible al jefe en pantalla."""
        self.visible = True

    def desaparecer(self):
        """Oculta al jefe (por ejemplo, al ser derrotado)."""
        self.visible = False

    def update(self):
        """Actualiza el comportamiento o animación del jefe."""
        pass
