import pyxel

class Juego:
    def __init__(self):
        self.puntuacion = 0
        self.fallos = 0
        pyxel.load("recursos.pyxres")

    def update(self):
        pass

    def dibujar(self):
        pyxel.cls(0)
