import pyxel

class Personaje:
    def __init__(self, nombre, x, y, u, v):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.u = u
        self.v = v

    def dibujar(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 16, 16)


mario = Personaje("Mario", 120, 100, 0, 0)
luigi = Personaje("Luigi", 120, 100, 16, 0)