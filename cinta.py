class Cinta:
    def __init__(self, id_cinta: int, x: int, y: int, longitud: int):
        self.id = id_cinta
        self.x = x               # Usa los setters con validación
        self.y = y
        self.longitud = longitud
        self.paquetes = []       # Lista de paquetes sobre la cinta

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

    # Propiedad y setter para Longitud
    @property
    def longitud(self) -> int:
        return self.__longitud

    @longitud.setter
    def longitud(self, longitud: int):
        if not isinstance(longitud, int):
            raise TypeError("La longitud debe ser un número entero, se recibió " + str(type(longitud)))
        elif longitud <= 0:
            raise ValueError("La longitud debe ser un número positivo mayor que cero")
        else:
            self.__longitud = longitud

    def update(self):
        pass
