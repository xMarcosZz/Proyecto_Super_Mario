import pyxel
from personajes import Personaje

def update():
    pass  # aquí luego irá el movimiento

def draw():
    pyxel.cls(0)  # limpia la pantalla con negro
    mario.dibujar()
    luigi.dibujar()

# Inicializa la ventana
pyxel.init(160, 120, title="Mario y Luigi - Prueba Personaje")
pyxel.load("recursos.pyxres")

# Crea los personajes
mario = Personaje("Mario", 120, 100, 0, 0)
luigi = Personaje("Luigi", 20, 100, 16, 0)

# Inicia el juego
pyxel.run(update, draw)
