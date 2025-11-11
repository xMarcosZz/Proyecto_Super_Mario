import pyxel
from Juego import Juego

if __name__ == "__main__":
    pyxel.init(256, 128,title="Mario Bros")
    juego = Juego()
    pyxel.run(juego.update, juego.draw)
