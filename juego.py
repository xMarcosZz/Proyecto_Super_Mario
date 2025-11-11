import pyxel
from Camion import Camion
from Cinta import Cinta
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe


class Juego:
    """Clase principal que gestiona el funcionamiento general del juego."""

    def __init__(self):
        """
        Método que inicializa todos los elementos del juego:
        carga los recursos gráficos, crea los objetos y configura las variables iniciales.
        """
        # --- Cargar los recursos del juego (.pyxres) ---
        pyxel.load("recursos.pyxres")

        # --- Variables del juego ---
        self.puntuacion = 0
        self.fallos = 0

        # --- Creación de los objetos principales ---
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)
        self.paquete = Paquete(26 * 8, 13 * 8)
        self.camion = Camion(1 * 8, 8 * 8)
        #self.jefe = Jefe(10 * 8, 5 * 8)

    # ---------------- MÉTODOS PRINCIPALES ---------------- #

    def update(self):
        """
        Este método se ejecuta en cada fotograma del juego (loop principal).
        Aquí se actualiza toda la lógica: movimiento, colisiones, puntuación, etc.
        """
        # Ejemplo: salir del juego con la tecla Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # En el futuro aquí se podrá incluir movimiento, colisiones, etc.
        # self.mario.mover()
        # self.paquete.update()
        pass

    def draw(self):
        """
        Este método dibuja en pantalla todos los elementos gráficos del juego
        en cada fotograma.
        """
        # Limpiar la pantalla (color de fondo 7 = gris claro)
        pyxel.cls(7)

        # --- Fondo (tilemap) ---
        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height
        pyxel.bltm(0, 0, 0, 0, 0, ancho, alto, colkey=7)

        # --- Marcadores de texto ---
        pyxel.text(200, 2, f"Puntos: {self.puntuacion}", 1)
        pyxel.text(200, 10, f"Fallos: {self.fallos}", 8)

        # --- Dibujar los objetos del juego ---
        pyxel.blt(self.camion.x, self.camion.y, *self.camion.sprite_camion)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite_mario)
        pyxel.blt(self.paquete.x,  self.paquete.y, *self.paquete.sprite_paquete)
