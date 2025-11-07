import pyxel
class Cinta:
    """
    Representa una cinta transportadora.
    Cada cinta puede tener paquetes moviéndose sobre ella.
    """
    def __init__(self, id_cinta, x, y, longitud):
        self.id = id_cinta
        self.x = x
        self.y = y
        self.longitud = longitud
        self.paquetes = []  # Lista de paquetes sobre la cinta

    def dibujar(self):
        pyxel.rect(self.x, self.y, self.longitud, 4, 11)
