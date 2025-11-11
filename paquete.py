class Paquete:
    def __init__(self, x: int, y: int):
        self.x = x   # Usa los setters con validación
        self.y = y
        self.activo = True  # Si se ha caído o entregado, será False
        self.sprite_paquete = (0, 32, 8, 8, 8, 7)

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

    def desactivar(self):
        """Desactiva el paquete (por ejemplo, si se cae o se entrega)."""
        self.activo = False

    def activar(self):
        """Reactiva el paquete (por ejemplo, al reiniciar el nivel)."""
        self.activo = True

    def update(self):
        """Actualiza el estado del paquete (caída, movimiento, etc)."""
        pass
