import pyxel
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe  # sigue ahí aunque aún no lo usemos mucho


class Juego:
    """Clase principal que gestiona el funcionamiento general del juego."""

    def __init__(self):
        """
        Inicializa todos los elementos del juego:
        carga recursos, crea objetos y configura variables.
        """
        # --- Cargar recursos de Pyxel --- #
        pyxel.load("recursos.pyxres")

        # --- Variables de juego --- #
        self.puntuacion = 0
        self.fallos = 0

        # --- Personajes --- #
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)

        # --- Paquete --- #
        self.paquete = Paquete(22 * 8, 13 * 8)

        # --- Camión --- #
        self.camion = Camion(1 * 8, 8 * 8)

        # --- Jefe (aún sin lógica de ataque) --- #
        self.jefe = Jefe(29 * 8, 12 * 8)

        # Coordenadas Y de los pisos (en píxeles, de abajo a arriba)
        self.pisos = [13 * 8, 9 * 8, 5 * 8]
        self.luigi.pisos = self.pisos
        self.mario.pisos = self.pisos

    # -------------------------- LOOP PRINCIPAL -------------------------- #

    def update(self):
        """Se ejecuta cada frame. Actualiza la lógica del juego."""
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # Actualizar personajes (subir/bajar pisos)
        self.actualizar_personajes()

        # Actualizar paquete con el recorrido completo
        self.paquete.update(self.mario, self.luigi, self)

    def draw(self):
        """Dibuja todos los elementos cada frame."""
        # Fondo blanco
        pyxel.cls(7)

        # --- Escenario (tilemap) --- #
        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height
        pyxel.bltm(0, 0, 0, 0, 0, ancho, alto, colkey=7)

        # --- Marcadores --- #
        pyxel.text(200, 2, f"Puntos: {self.puntuacion}", 1)
        pyxel.text(200, 10, f"Fallos: {self.fallos}", 8)

        # --- Dibujar objetos --- #
        # Camión
        pyxel.blt(self.camion.x, self.camion.y, *self.camion.sprite_camion)

        # Personajes
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite_mario)

        # Paquete
        self.paquete.draw()

        # (Opcional) jefe, si quieres que se vea ya
        # if self.jefe.visible:
        #     pyxel.blt(self.jefe.x, self.jefe.y, *self.jefe.sprite_jefe)

    # -------------------- CONTROLES DE LOS PERSONAJES -------------------- #

    def actualizar_personajes(self):
        # Mario: flechas
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover_abajo()

        # Luigi: WASD
        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover_abajo()
