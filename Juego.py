import pyxel
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe


class Juego:

    def __init__(self):
        pyxel.load("recursos.pyxres")

        self.puntuacion = 0
        self.fallos = 0

        # Variable de fin del juego
        self.game_over = False

        self.camion = Camion(1 * 8, 8 * 8)
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)
        self.paquete = Paquete(32 * 8, 13 * 8)
        self.jefe = Jefe(29 * 8, 12 * 8)

        self.pisos = [13 * 8, 8 * 8, 4 * 8]
        self.mario.pisos = self.pisos
        self.luigi.pisos = self.pisos

    # --------------------------------------------------

    def update(self):

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # ════════════════════════════════
        #   FIN DEL JUEGO (3 FALLOS)
        # ════════════════════════════════
        if self.fallos >= 3:
            self.game_over = True

        if self.game_over:
            return  # pausa todo

        # ════════════════════════════════
        #   ACTUALIZAR CAMIÓN
        # ════════════════════════════════
        self.camion.update()

        # Si terminó el reparto → reaparece paquete
        if self.camion.reparto_terminado:
            self.camion.reparto_terminado = False
            self.paquete.reiniciar_salida()
            self.paquete.activo = True
            self.paquete.estado = "salida"
            self.paquete.piso = 0
            self.paquete.vx = -self.paquete.VX

        # Si camión está fuera → pausa juego
        if self.camion.estado == "fuera":
            return

        # ════════════════════════════════
        #   ACTUALIZAR PERSONAJES
        # ════════════════════════════════
        self.actualizar_personajes()

        # ════════════════════════════════
        #   ACTUALIZAR PAQUETE
        # ════════════════════════════════
        self.paquete.update(self.mario, self.luigi, self)

    # --------------------------------------------------

    def draw(self):
        pyxel.cls(7)

        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height
        pyxel.bltm(0, 0, 0, 0, 0, ancho, alto, colkey=7)

        # Indicadores
        pyxel.text(200, 2, f"Puntos: {self.puntuacion}", 1)
        pyxel.text(200, 10, f"Fallos: {self.fallos}", 8)
        pyxel.text(200, 18, f"Camion: {self.camion.carga}/8", 1)

        # DIBUJAR LAS CRUCES DE FALLOS
        self.dibujar_cruces_fallos()

        # Objetos del juego
        self.camion.draw()
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite_mario)
        self.paquete.draw()

        # Mensaje mientras camión está de reparto
        if self.camion.estado == "fuera":
            pyxel.text(70, 60, "EL CAMION ESTA EN REPARTO...", 8)

        # FIN DEL JUEGO
        if self.game_over:
            pyxel.rect(40, 40, 160, 40, 0)
            pyxel.text(80, 60, "  FIN DEL JUEGO", 8)
            return

    # --------------------------------------------------

    def dibujar_cruces_fallos(self):
        """Dibuja las X encima de las cabezas según los fallos."""
        posiciones_x = [17 * 8, 19 * 8, 21 * 8]

        for i in range(min(self.fallos, 3)):
            pyxel.text(posiciones_x[i], 0, "X", 8)  # color rosa fuerte

    # --------------------------------------------------

    def actualizar_personajes(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover_abajo()

        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover_abajo()
