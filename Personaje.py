import pyxel

class Personaje:
    def __init__(self,nombre,x,y):
        self.nombre=nombre
        self.x=x
        self.y=y
        self.piso=0
    def update(self):
        pass
    def dibujar(self):
     # Si el nombre es Luigi (izquierda, azul)
        if self.nombre.lower() == "luigi":
            # Luigi está a la izquierda → debe mirar hacia la derecha
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, 7)
        else:
            # Mario (derecha, morado) → debe mirar hacia la izquierda
            pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 7)


