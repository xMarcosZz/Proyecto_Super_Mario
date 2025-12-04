"""
Juego.py
--------
Módulo principal de la lógica del juego.

Gestiona:
- La creación de objetos (camión, personajes, paquete, jefe).
- El bucle principal de actualización (`update`).
- El dibujado en pantalla (`draw`).
- El control de fallos, puntuación, reparto del camión
  y la lógica de GAME OVER y reinicio.
"""

import pyxel
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe


class Juego:
    """
    Clase principal del juego.

    Coordina todos los objetos:
    - Camión
    - Mario y Luigi
    - Paquete
    - Jefe (aparece tras fallos)
    - Estados globales del juego
    """

    def __init__(self):
        """Inicializa el juego, sus objetos y las variables globales."""
        pyxel.load("recursos.pyxres")

        # Marcadores
        self.puntuacion = 0
        self.fallos = 0

        # Variables de control
        self.game_over = False
        self.jefe_timer = 0          # frames que el jefe estará activo
        self.jefe_duracion = 120     # 2 segundos a 60 FPS
        self.shake = 0               # intensidad del temblor de pantalla

        # Objetos principales
        self.camion = Camion(1 * 8, 8 * 8)
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)
        self.paquete = Paquete(32 * 8, 13 * 8)

        # Jefe animado en la parte superior
        self.jefe = Jefe(15 * 8, 3 * 8)
        self.jefe.desaparecer()

        # Altura en píxeles de los 3 pisos
        self.pisos = [13 * 8, 8 * 8, 4 * 8]
        self.mario.pisos = self.pisos
        self.luigi.pisos = self.pisos

    # ================================================================
    #   MÉTODO PRINCIPAL DE UPDATE
    # ================================================================

    def update(self):
        """Actualiza el estado del juego en cada frame."""

        # Salida del juego
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # 1) GAME OVER: solo escuchar tecla R
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reiniciar_partida()
            return

        # 2) Si se llega a 3 fallos → activar GAME OVER
        if self.fallos >= 3:
            self.game_over = True
            return

        # 3) Actualización cuando el jefe está visible (pausa fuerte)
        if self._update_jefe_activo():
            return

        # 4) Actualización del camión (puede pausar el juego)
        if self._update_camion():
            return

        # 5) Movimiento de personajes
        self._update_personajes()

        # 6) Movimiento del paquete
        self.paquete.update(self.mario, self.luigi, self)

        # 7) Animación del jefe si sigue visible
        self.jefe.update()

    # ================================================================
    #   SUBMÉTODOS DE UPDATE
    # ================================================================

    def _update_jefe_activo(self) -> bool:
        """
        Si el jefe está activo:
        - Se anima.
        - Se deja caer el paquete si estaba en caida_fallo.
        - La pantalla tiembla.
        - El resto del juego queda pausado.

        Devuelve True si el juego sigue en pausa.
        """
        if self.jefe_timer <= 0:
            return False

        self.jefe_timer -= 1
        self.jefe.update()

        # Permitir que el paquete termine su animación de caída
        self.paquete.update(self.mario, self.luigi, self)

        # Activa temblor
        self.shake = 3

        # Cuando el tiempo termina → apagar jefe
        if self.jefe_timer <= 0:
            self.jefe.desaparecer()
            self.shake = 0

            # Si el paquete "murió" en la caída, generamos otro
            if not self.paquete.activo:
                self.paquete.reiniciar_salida()
                self.paquete.activo = True

        return True

    def _update_camion(self) -> bool:
        """
        Actualiza el estado del camión:
        - Salida a reparto
        - Pausa del juego mientras está fuera
        - Regreso

        Devuelve True si el juego debe pausarse (camión fuera).
        """
        self.camion.update()

        # Si terminó un reparto, reiniciar paquete
        if self.camion.reparto_terminado:
            self.camion.reparto_terminado = False

            if self.paquete.estado == "entrega":
                self.paquete.reiniciar_salida()

        # Si el camión está fuera → pausar el juego
        if self.camion.estado == "fuera":
            return True

        return False

    def _update_personajes(self):
        """Lee los controles y mueve a Mario y Luigi entre pisos."""

        # Mario con flechas ↑ ↓
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover_abajo()

        # Luigi con W / S
        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover_abajo()

    # ================================================================
    #   DIBUJADO
    # ================================================================

    def draw(self):
        """Dibuja todos los elementos del juego y el HUD."""
        pyxel.cls(7)

        # Temblor mientras aparece el jefe
        dx = dy = 0
        if self.jefe_timer > 0:
            dx = pyxel.rndi(-self.shake, self.shake)
            dy = pyxel.rndi(-self.shake, self.shake)

        # Dibujo del tilemap de fondo
        ancho = pyxel.tilemaps[0].width
        alto = pyxel.tilemaps[0].height
        pyxel.bltm(dx, dy, 0, 0, 0, ancho, alto, colkey=7)

        # HUD
        pyxel.text(200, 2, f"Puntos: {self.puntuacion}", 1)
        pyxel.text(200, 10, f"Fallos: {self.fallos}", 8)
        pyxel.text(200, 18, f"Camion: {self.camion.carga}/8", 1)

        self.dibujar_cruces_fallos()

        # Objetos principales
        self.camion.draw()
        self.jefe.draw()
        pyxel.blt(self.luigi.x + dx, self.luigi.y + dy, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x + dx, self.mario.y + dy, *self.mario.sprite_mario)
        self.paquete.draw()

        # Mensaje de reparto
        if self.camion.estado == "fuera":
            pyxel.text(70, 60, "EL CAMION ESTA EN REPARTO...", 8)

        # GAME OVER
        if self.game_over:
            self._draw_game_over()

    # ================================================================
    #   DIBUJO AUXILIAR
    # ================================================================

    def dibujar_cruces_fallos(self):
        """Dibuja una X por cada fallo del jugador."""
        posiciones_x = [17 * 8, 19 * 8, 21 * 8]

        for i in range(min(self.fallos, 3)):
            pyxel.text(posiciones_x[i], 0, "X", 8)

    def _draw_game_over(self):
        """Dibuja la ventana de GAME OVER."""
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)

        panel_x, panel_y = 40, 40
        panel_w, panel_h = 160, 60

        pyxel.rect(panel_x - 2, panel_y - 2, panel_w + 4, panel_h + 4, 8)
        pyxel.rect(panel_x, panel_y, panel_w, panel_h, 0)

        pyxel.text(panel_x + 35, panel_y + 15, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(panel_x + 20, panel_y + 35, "Pulsa R para reiniciar", 7)

    # ================================================================
    #   EVENTOS ESPECIALES
    # ================================================================

    def invocar_jefe(self):
        """Hace aparecer al jefe cuando hay un fallo."""
        self.jefe.aparecer()
        self.jefe_timer = self.jefe_duracion
        self.shake = 3

    def reiniciar_partida(self):
        """Restaura todas las variables al estado inicial."""

        # Marcadores
        self.puntuacion = 0
        self.fallos = 0
        self.game_over = False

        # Camión
        self.camion.carga = 0
        self.camion.estado = Camion.PARADO
        self.camion.x = 1 * 8
        self.camion.y = 8 * 8
        self.camion.reparto_terminado = False

        # Paquete
        self.paquete.reiniciar_salida()
        self.paquete.activo = True

        # Personajes
        self.mario.piso = 0
        self.luigi.piso = 0
        self.mario.y = self.pisos[0]
        self.luigi.y = self.pisos[0]

        # Jefe
        self.jefe.desaparecer()
        self.jefe_timer = 0
        self.shake = 0
