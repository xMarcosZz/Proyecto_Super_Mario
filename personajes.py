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
        # Si el nombre es Luigi (izquierda, azul)
        if self.nombre.lower() == "luigi":
            # Luigi está a la izquierda → debe mirar hacia la derecha
            pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)
        else:
            # Mario (derecha, morado) → debe mirar hacia la izquierda
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, 0)

    def mover_arriba(self):
        """Sube un piso (más adelante verificaremos límites)."""
        pass

    def mover_abajo(self):
        """Baja un piso."""
        pass
