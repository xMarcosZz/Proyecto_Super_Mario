import pyxel
class Camion:
    """
    Representa el camión de reparto.
    Guarda cuántos paquetes lleva cargados.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.carga = 0  # Paquetes entregados

    def dibujar(self):
        pyxel.rect(self.x, self.y, 30, 12, 8)  # cuerpo
        pyxel.circ(self.x + 5, self.y + 12, 2, 0)  # ruedas
        pyxel.circ(self.x + 25, self.y + 12, 2, 0)

