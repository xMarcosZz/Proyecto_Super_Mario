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

        # Variables de control
        self.game_over = False
        self.jefe_timer = 0           # frames que el jefe estará activo
        self.jefe_duracion = 120      # 2 segundos a 60 FPS
        self.shake = 0                # temblor

        # Objetos principales
        self.camion = Camion(1 * 8, 8 * 8)
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)
        self.paquete = Paquete(32 * 8, 13 * 8)

        # Jefe
        self.jefe = Jefe(15 * 8, 3 * 8)
        self.jefe.desaparecer()

        self.pisos = [13 * 8, 8 * 8, 4 * 8]
        self.mario.pisos = self.pisos
        self.luigi.pisos = self.pisos

    # --------------------------------------------------

    def update(self):

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # Fin del juego
        if self.fallos >= 3:
            self.game_over = True

        if self.game_over:
            return

        # ─────────────────────────────────────────────
        # PAUSA TOTAL mientras el jefe está activo
        # ─────────────────────────────────────────────
        if self.jefe_timer > 0:
            self.jefe_timer -= 1
            self.jefe.update()

            # Temblor suave mientras aparece el jefe
            self.shake = 3

            if self.jefe_timer <= 0:
                self.jefe.desaparecer()
                self.shake = 0

            return  # ← PAUSA TOTAL DEL JUEGO

        # ─────────────────────────────────────────────
        # ACTUALIZAR CAMIÓN
        # ─────────────────────────────────────────────
        self.camion.update()

        if self.camion.reparto_terminado:
            self.camion.reparto_terminado = False
            if self.paquete.estado == "entrega":
                self.paquete.reiniciar_salida()

        if self.camion.estado == "fuera":
            return

        # ─────────────────────────────────────────────
        # ACTUALIZAR PERSONAJES
        # ─────────────────────────────────────────────
        self.actualizar_personajes()

        # ─────────────────────────────────────────────
        # ACTUALIZAR PAQUETE
        # ─────────────────────────────────────────────
        self.paquete.update(self.mario, self.luigi, self)

        # Actualizar animación del jefe si estuviera visible
        self.jefe.update()

    # --------------------------------------------------

    def draw(self):
        pyxel.cls(7)

        # Temblor mientras el jefe está en pantalla
        dx = dy = 0
        if self.jefe_timer > 0:
            dx = pyxel.rndi(-self.shake, self.shake)
            dy = pyxel.rndi(-self.shake, self.shake)

        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height

        pyxel.bltm(dx, dy, 0, 0, 0, ancho, alto, colkey=7)

        pyxel.text(200, 2, f"Puntos: {self.puntuacion}", 1)
        pyxel.text(200, 10, f"Fallos: {self.fallos}", 8)
        pyxel.text(200, 18, f"Camion: {self.camion.carga}/8", 1)

        self.dibujar_cruces_fallos()

        # Dibujar objetos
        self.camion.draw()
        pyxel.blt(self.luigi.x + dx, self.luigi.y + dy, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x + dx, self.mario.y + dy, *self.mario.sprite_mario)
        self.paquete.draw()
        self.jefe.draw()

        # Mensaje de reparto
        if self.camion.estado == "fuera":
            pyxel.text(70, 60, "EL CAMION ESTA EN REPARTO...", 8)

        # Fin de juego
        if self.game_over:
            pyxel.rect(40, 40, 160, 40, 0)
            pyxel.text(80, 60, "  FIN DEL JUEGO", 8)

    # --------------------------------------------------

    def dibujar_cruces_fallos(self):
        posiciones_x = [17 * 8, 19 * 8, 21 * 8]
        for i in range(min(self.fallos, 3)):
            pyxel.text(posiciones_x[i], 0, "X", 8)

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

    # --------------------------------------------------

    def invocar_jefe(self):
        """El jefe aparece cuando hay un fallo."""
        self.jefe.aparecer()
        self.jefe_timer = self.jefe_duracion
        self.shake = 3   # temblor
