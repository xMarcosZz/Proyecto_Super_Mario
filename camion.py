import pyxel
class Camion:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.carga = 0  # Paquetes entregados

    def dibujar(self):
        pyxel.blt(self.x,self.y,0,16,32,24,16)