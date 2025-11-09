import pyxel
class Paquete:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activo = True  # Si se ha caído o entregado, será False

    def dibujar(self):
        if self.activo:
            pyxel.blt(self.x,self.y,0,32,8,8,8,7)