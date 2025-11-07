import pyxel
class Personaje:
    """
    Clase base para todos los personajes (Mario y Luigi).
    Contendrá su posición, piso actual y métodos comunes.
    """
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.piso = 0  # Piso inicial

    def dibujar(self):
        # Según el nombre elegimos el sprite
        if self.nombre.lower() == "luigi":
            pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, 0)

    def mover_arriba(self):
        """Sube un piso (más adelante verificaremos límites)."""
        pass

    def mover_abajo(self):
        """Baja un piso."""
        pass
