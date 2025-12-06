import pyxel


class GestorSonido:
    """
    Clase encargada de gestionar todo el audio del juego.
    Define los sonidos en el init y ofrece métodos públicos
    para reproducirlos desde otras partes del código.
    """

    def __init__(self):
        """Constructor: Inicializa los bancos de sonido."""
        self._init_bancos()

    def _init_bancos(self):
        """
        Define las notas y efectos en los bancos de memoria de Pyxel.
        """
        # ------------------------------------------------
        # EFECTOS DE SONIDO (SFX)
        # ------------------------------------------------

        # Sonido 0: Entrega correcta (sonido tipo moneda/agudo)
        # Notas: Do3, Mi3, Sol3, Do4. Tono: Triangle.
        pyxel.sound(0).set("c3e3g3c4", "t", "6", "vffn", 25)

        # Sonido 1: Fallo (ruido grave)
        # Notas: Do2, Do1. Tono: Noise (ruido).
        pyxel.sound(1).set("c2c1", "n", "77", "vffn", 25)

        # Sonido 2: Game Over (melodía triste descendente)
        # Notas: Do3, Sol2, Mi2, Do2. Tono: Square.
        pyxel.sound(2).set("c3g2e2c2", "s", "6", "vffn", 30)

        # ------------------------------------------------
        # MÚSICA DE FONDO (BGM)
        # ------------------------------------------------

        # Sonido 10: Melodía principal (Parte A)
        pyxel.sound(10).set(
            "e3e3r c3e3g3r g2r c3g2e2 a2b2a2g2",
            "s", "4", "nnnf", 11
        )

        # Sonido 11: Melodía principal (Parte B - Variación)
        pyxel.sound(11).set(
            "c3r g2e2a2b2 a2g2e3g3 a3f3g3e3 c3d3b2c3",
            "s", "4", "nnnf", 11
        )

        # Sonido 12: Bajo rítmico (Acompañamiento)
        pyxel.sound(12).set(
            "c2r g1r c2r g1r f1r c2r f1r c2r",
            "t", "6", "n", 11
        )

    def reproducir_musica_juego(self):
        """Inicia la música de fondo en bucle."""
        # Canal 0: Reproduce la melodía (sonidos 10 y 11) en bucle
        pyxel.play(0, [10, 11], loop=True)

        # Canal 1: Reproduce el bajo (sonido 12) en bucle
        pyxel.play(1, [12, 12], loop=True)

    def detener_musica(self):
        """Silencia todos los canales de audio."""
        pyxel.stop()

    def sfx_entrega(self):
        """Reproduce el sonido de entrega exitosa."""
        pyxel.play(0, 0)

    def sfx_fallo(self):
        """Reproduce el sonido de error."""
        # Usamos el canal 0 para interrumpir momentáneamente la melodía
        pyxel.play(0, 1)

    def sfx_game_over(self):
        """Detiene la música y reproduce el sonido de fin de juego."""
        self.detener_musica()
        pyxel.play(0, 2)