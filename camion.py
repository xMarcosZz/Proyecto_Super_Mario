class Camion:
    def __init__(self, x: int, y: int):
        self.x = x  # Usa los setters con validación
        self.y = y
        self.carga = 0  # Paquetes entregados
        self.sprite_camion = (0, 16, 32, 24, 16)

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

    def update(self):
        pass

