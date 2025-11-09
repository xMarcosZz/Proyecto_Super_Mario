import pyxel
from Camion import Camion
from Cinta import Cinta
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe


class Juego:
    #Crearemos los objetos
    def __init__(self):
        pyxel.load("recursos.pyxres")
        # Variables del juego
        self.puntuacion = 0
        self.fallos = 0
        # Objetos del juego
        self.mario=Personaje("Mario",24*8,13*8)
        self.luigi=Personaje("Luigi",6*8,13*8)
        self.paquete = Paquete(26*8,13*8)
        self.camion = Camion(3,8*8)
    def update(self):
        pass

    def draw(self):

        pyxel.cls(7)
        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height
        pyxel.bltm(0, 0, 0, 0, 0, ancho, alto,7)
        # --- Texto marcador ---
        pyxel.text(200, 20, f"Puntos: {self.puntuacion}", 1)
        pyxel.text(200, 6, f"Fallos: {self.fallos}", 8)

        self.mario.dibujar()
        self.luigi.dibujar()
        self.paquete.dibujar()
        self.camion.dibujar()

