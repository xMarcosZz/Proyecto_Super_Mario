import pyxel
class Paquete:
    """
    Representa un paquete (caja) que se moverá por las cintas.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activo = True  # Si se ha caído o entregado, será False

    def dibujar(self):
        if self.activo:
            pass