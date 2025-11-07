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
        self.mario = Personaje("Mario", 200, 140)
        self.luigi = Personaje("Luigi", 40, 140)
        self.camion = Camion(10, 120)
        self.paquete = Paquete(100, 132)

    def update(self):
        """Por ahora no hay lógica de movimiento."""
        pass

    def draw(self):
        """Dibuja el tilemap y los personajes sobre él."""
        pyxel.cls(0)

        # --- Muestra el TILEMAP 0 completo ---
        # Cada tile = 8x8 píxeles, así que para cubrir 256x192 son 32x24 tiles
        pyxel.bltm(0, 0, 0, 0, 0, 32, 24)

        # --- Dibuja tus personajes y elementos sobre el fondo ---
        self.camion.dibujar()
        self.paquete.dibujar()
        self.mario.dibujar()
        self.luigi.dibujar()

        # --- Marcador arriba ---
        pyxel.text(6, 6, f"Puntos: {self.puntuacion}", 7)
        pyxel.text(180, 6, f"Fallos: {self.fallos}", 8)
