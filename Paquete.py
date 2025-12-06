import pyxel

class Paquete:
    """
    Controla el comportamiento del paquete:
    - Recorrido completo en los 3 pisos.
    - Respeto de la columna morada (teletransporte).
    - Subida automática entre pisos.
    - Entrega al camión.
    - Caída cuando ocurre un fallo.
    """

    # --- CONSTANTES DE POSICIÓN ---
    PISOS_Y = [13, 9, 5]

    COL_SALIDA_X = 32
    COL_STOP_MARIO = 26
    COL_MARIO_X = 24
    COL_LUIGI_X = 6

    COL_COL_CONTACTO_DER = 17
    COL_COL_DETRAS_IZQ = 14

    COL_COL_CONTACTO_IZQ = 14
    COL_COL_DETRAS_DER = 17

    COL_FINAL_LUIGI = 9
    COL_FINAL_MARIO_P1 = 21

    POS_INICIO_CINTA = [
        (22, 13),  # piso 0 → pasa al 1
        (10, 9),   # piso 1 → pasa al 2
        (22, 5)    # piso 2 → entrega
    ]

    CAMION_X = 3
    CAMION_Y = 5

    # Velocidades (modificadas por menú)
    VX = 2.5
    VY_CAIDA = 1

    # --------------------------------------------------------------

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_real = float(x)
        self.y_real = float(y)

        self.sprite_paquete = (0, 32, 8, 8, 8, 7)

        self.vx = -self.VX
        self.vy = 0.0

        self.estado = "salida"
        self.piso = 0
        self.activo = True

    # ---------------- PROPIEDADES X/Y ----------------

    @property
    def x(self): return self.__x
    @x.setter
    def x(self, v): self.__x = int(v)

    @property
    def y(self): return self.__y
    @y.setter
    def y(self, v): self.__y = int(v)

    # --------------------------------------------------
    #   REINICIO
    # --------------------------------------------------

    def reiniciar_salida(self):
        """Coloca el paquete en el inicio del recorrido."""
        self.estado = "salida"
        self.piso = 0
        self.vx = -self.VX
        self.vy = 0.0
        self.x_real = self.COL_SALIDA_X * 8
        self.y_real = self.PISOS_Y[0] * 8
        self.x = self.x_real
        self.y = self.y_real
        self.activo = True

    # --------------------------------------------------
    #   UPDATE PRINCIPAL
    # --------------------------------------------------

    def update(self, mario, luigi, juego):

        if not self.activo:
            return

        # ======================================================
        #   CAÍDA DE FALLO
        # ======================================================
        if self.estado == "caida_fallo":
            self.y_real += self.vy
            self.y = self.y_real

            if self.y > pyxel.height:
                if juego.jefe_timer > 0:
                    self.activo = False
                else:
                    self.reiniciar_salida()
            return

        # ======================================================
        #  ESTADO: SALIDA (32 → 26)
        # ======================================================
        if self.estado == "salida":
            self.piso = 0
            self.y_real = self.PISOS_Y[0] * 8
            self.y = self.y_real

            self.vx = -self.VX
            self.x_real += self.vx
            self.x = self.x_real

            if self.x <= self.COL_STOP_MARIO * 8:
                if mario.piso != 0:
                    juego.fallos += 1
                    juego.invocar_jefe()
                    self._fallar()
                    return

                self.estado = "salida_detras_mario"

        # ======================================================
        #  DETRÁS DE MARIO
        # ======================================================
        elif self.estado == "salida_detras_mario":

            self.x_real += self.vx
            self.x = self.x_real

            pos_detras = (self.COL_MARIO_X + 1) * 8

            if self.x <= pos_detras:

                if mario.piso != 0:
                    juego.fallos += 1
                    juego.invocar_jefe()
                    self._fallar()
                    return

                self.x_real = 22 * 8
                self.y_real = 13 * 8
                self.x = self.x_real
                self.y = self.y_real

                self.estado = "a_columna"

        # ======================================================
        #  HACIA LA COLUMNA MORADA
        # ======================================================
        elif self.estado == "a_columna":

            # Piso 1 → derecha
            if self.piso == 1:
                self.vx = abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                if self.x >= self.COL_COL_CONTACTO_IZQ * 8:
                    self.x_real = self.COL_COL_DETRAS_DER * 8
                    self.x = self.x_real
                    self.estado = "a_destino"

            # Pisos 0 y 2 → izquierda
            else:
                self.vx = -abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                if self.x <= self.COL_COL_CONTACTO_DER * 8:
                    self.x_real = self.COL_COL_DETRAS_IZQ * 8
                    self.x = self.x_real
                    self.estado = "a_destino"

        # ======================================================
        #   DESTINO FINAL DEL PISO
        # ======================================================
        elif self.estado == "a_destino":

            # Piso 1 → hacia Mario
            if self.piso == 1:

                self.vx = abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                final_x = self.COL_FINAL_MARIO_P1 * 8

                if self.x >= final_x:

                    if mario.piso != 1:
                        juego.fallos += 1
                        juego.invocar_jefe()
                        self._fallar()
                        return

                    self.piso = 2
                    self._tp_principio_cinta()
                    self.estado = "a_columna"

            # Piso 0 y 2 → hacia Luigi
            else:
                self.vx = -abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                final_x = self.COL_FINAL_LUIGI * 8

                if self.x <= final_x:

                    # Piso 0 → Luigi debe estar
                    if self.piso == 0:

                        if luigi.piso != 0:
                            juego.fallos += 1
                            juego.invocar_jefe()
                            self._fallar()
                            return

                        self.piso = 1
                        self._tp_principio_cinta()
                        self.estado = "a_columna"

                    # Piso 2 → entrega
                    else:

                        if luigi.piso != 2:
                            juego.fallos += 1
                            juego.invocar_jefe()
                            self._fallar()
                            return

                        self.estado = "entrega"
                        self._tp_sobre_camion()

        # ======================================================
        #   ENTREGA FINAL
        # ======================================================
        elif self.estado == "entrega":

            self.y_real += self.VY_CAIDA
            self.y = self.y_real

            if self.y >= self.CAMION_Y * 8:

                juego.puntuacion += 1
                juego.camion.carga += 1

                if juego.camion.carga >= 8:
                    juego.puntuacion += 10
                    juego.camion.carga = 0
                    juego.camion.iniciar_reparto()

                self.reiniciar_salida()

    # --------------------------------------------------
    #   AUXILIARES
    # --------------------------------------------------

    def _tp_principio_cinta(self):
        x_tile, y_tile = self.POS_INICIO_CINTA[self.piso]
        self.x_real = x_tile * 8
        self.y_real = y_tile * 8
        self.x = self.x_real
        self.y = self.y_real

    def _tp_sobre_camion(self):
        self.x_real = self.CAMION_X * 8
        self.y_real = (self.CAMION_Y - 4) * 8
        self.x = self.x_real
        self.y = self.y_real
        self.vy = self.VY_CAIDA

    def _fallar(self):
        self.estado = "caida_fallo"
        self.vx = 0.0
        self.vy = self.VY_CAIDA

    # --------------------------------------------------
    #   DRAW
    # --------------------------------------------------

    def draw(self):
        if self.activo:
            pyxel.blt(self.x, self.y, *self.sprite_paquete)
