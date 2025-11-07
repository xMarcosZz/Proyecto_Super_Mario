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
        pass