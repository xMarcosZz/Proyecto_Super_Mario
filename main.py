import pyxel
from juego import Juego

if __name__ == "__main__":
    # Tamaño 256x192 (clásico Pyxel)
    pyxel.init(256, 192, title="Proyecto Mario Bros")
    juego = Juego()
    pyxel.run(juego.update, juego.draw)
