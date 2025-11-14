class Personaje:
    def __init__(self, nombre: str, x: int, y: int):
        self.nombre = nombre
        self.x = x  # Usa el setter con validación
        self.y = y  # Usa el setter con validación

        self.sprite_luigi = (0, 16, 0, 16, 16, 7)
        self.sprite_mario = (0, 0, 0, 16, 16, 7)
        self.piso = 0
        self.pisos = None


    # Propiedad y setter para X
    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("La coordenada X debe ser un número entero")
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
            raise TypeError("La coordenada Y debe ser un número entero")
        elif y < 0:
            raise ValueError("La coordenada Y debe ser un número no negativo")
        else:
            self.__y = y

    def mover_arriba(self):
        if self.piso < len(self.pisos) - 1:  # si no está ya arriba del todo
            self.piso += 1  # cambia al piso superior
            self.y = self.pisos[self.piso]  # coloca al personaje en la altura correcta

    def mover_abajo(self):
        if self.piso > 0:  # si no está ya en el piso inferior
            self.piso -= 1  # baja un piso
            self.y = self.pisos[self.piso]
