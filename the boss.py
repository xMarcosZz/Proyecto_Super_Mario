import pyxel

class TheBoss:
    """
    Representa al jefe que lanza los paquetes desde arriba.
    En el Sprint 1 solo se dibuja; en los siguientes podrá lanzar paquetes.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True  # Por si luego quieres hacerlo aparecer/desaparecer

    def dibujar(self):
        """Dibuja al jefe en la parte superior del escenario."""
        if not self.visible:
            return

        # Dibuja el sprite del jefe desde recursos.pyxres
        # (ajusta u, v, w, h según la posición real en tu hoja de sprites)
        pyxel.blt(self.x, self.y, 0, 64, 0, 16, 16, 0)
