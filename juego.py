import pyxel
from personajes import Personaje
from cinta import Cinta
from paquete import Paquete
from camion import Camion

class Juego:
    def __init__(self):
        # Cargamos tu .pyxres (el mismo donde está tu tilemap)
        pyxel.load("recursos.pyxres")

        # Variables del juego
        self.puntuacion = 0
        self.fallos = 0

        # Creamos objetos principales (los usaremos más adelante)
        self.mario = Personaje("Mario", 40, 140)
        self.luigi = Personaje("Luigi", 200, 140)
        self.camion = Camion(10, 120)
        self.paquete = Paquete(100, 132)
        print("Contenido del tilemap:", pyxel.tilemaps[0].pget(0, 0))

    def update(self):
        """Por ahora no hay lógica de movimiento."""
        pass

    def draw(self):
        # Limpia fondo blanco
        pyxel.cls(7)

        # --- Dibuja TODO el Tilemap 0 completo ---
        # Para cubrir toda la pantalla, usamos el tamaño del tilemap en tiles
        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height
        pyxel.bltm(0, 0, 0, 0, 0, ancho, alto)

        # --- Personajes y objetos ---
        self.camion.dibujar()
        self.paquete.dibujar()
        self.mario.dibujar()
        self.luigi.dibujar()

        # --- Texto marcador ---
        pyxel.text(6, 6, f"Puntos: {self.puntuacion}", 7)
        pyxel.text(200, 6, f"Fallos: {self.fallos}", 8)

        pyxel.bltm(0, 0, 0, 8, 8, 32, 24)
