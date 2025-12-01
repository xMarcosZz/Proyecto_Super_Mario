import pyxel


class Paquete:
    """
    Gestiona todo el recorrido del paquete:
    - Salida desde la derecha (piso 0)
    - Mario / Luigi lo recogen según el piso
    - Se mueve por las cintas respetando la columna central
    - Subida de piso cuando el personaje correspondiente sube
    - Entrega final al camión en el piso 2
    """

    # --- COORDENADAS DE REFERENCIA (TILES) --- #
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

    POS_INICIO_CINTA = [(22, 13), (10, 9), (22, 5)]

    CAMION_X = 3
    CAMION_Y = 5

    VX = 2.5
    VY_CAIDA = 1

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

    # ---------------- PROPIEDADES ---------------- #

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, v):
        self.__x = int(v)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, v):
        self.__y = int(v)

    # ---------------- REINICIO ---------------- #

    def reiniciar_salida(self):
        self.estado = "salida"
        self.piso = 0
        self.vx = -self.VX
        self.vy = 0.0
        self.x_real = self.COL_SALIDA_X * 8
        self.y_real = self.PISOS_Y[0] * 8
        self.x = self.x_real
        self.y = self.y_real

    # ---------------- UPDATE PRINCIPAL ---------------- #

    def update(self, mario, luigi, juego):
        if not self.activo:
            return

        # ==========================================================
        #  ESTADO: CAÍDA POR FALLO
        # ==========================================================
        if self.estado == "caida_fallo":
            self.y_real += self.vy
            self.y = self.y_real

            if self.y > pyxel.height:
                # La caja ya ha salido de la pantalla
                # Mientras el jefe siga en pantalla → no generes otra
                if juego.jefe_timer > 0:
                    self.activo = False  # se desactiva y se queda "muerta"
                else:
                    # Si ya no hay jefe, se puede reiniciar normalmente
                    self.reiniciar_salida()

            return

        # ==========================================================
        #  ESTADO 1 — SALIDA 32→26
        # ==========================================================
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
                    juego.invocar_jefe()     # ★ INVOCAR JEFE
                    self._iniciar_caida_fallo()
                    return

                self.estado = "salida_detras_mario"

        # ==========================================================
        #  ESTADO 2 — LLEGAR DETRÁS DE MARIO
        # ==========================================================
        elif self.estado == "salida_detras_mario":

            self.vx = -self.VX
            self.x_real += self.vx
            self.x = self.x_real

            x_detras_mario = (self.COL_MARIO_X + 1) * 8

            if self.x <= x_detras_mario:

                if mario.piso != 0:
                    juego.fallos += 1
                    juego.invocar_jefe()     # ★ INVOCAR JEFE
                    self._iniciar_caida_fallo()
                    return

                self.x_real = 22 * 8
                self.y_real = 13 * 8
                self.x = self.x_real
                self.y = self.y_real

                self.estado = "a_columna"
                self.vx = -self.VX

        # ==========================================================
        #  ESTADO 3 — LLEGAR A LA COLUMNA
        # ==========================================================
        elif self.estado == "a_columna":

            if self.piso == 1:  # PISO 1 → derecha
                self.vx = abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                if self.x >= self.COL_COL_CONTACTO_IZQ * 8:
                    self.x_real = self.COL_COL_DETRAS_DER * 8
                    self.x = self.x_real
                    self.estado = "a_destino"

            else:  # pisos 0 y 2 → izquierda
                self.vx = -abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                if self.x <= self.COL_COL_CONTACTO_DER * 8:
                    self.x_real = self.COL_COL_DETRAS_IZQ * 8
                    self.x = self.x_real
                    self.estado = "a_destino"

        # ==========================================================
        #  ESTADO 4 — COLUMNA → DESTINO
        # ==========================================================
        elif self.estado == "a_destino":

            # ------------ PISO 1 → hacia Mario ------------ #
            if self.piso == 1:
                self.vx = abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                final_x = self.COL_FINAL_MARIO_P1 * 8

                if self.x >= final_x:

                    if mario.piso != self.piso:
                        juego.fallos += 1
                        juego.invocar_jefe()     # ★ INVOCAR JEFE
                        self._iniciar_caida_fallo()
                        return

                    self.estado = "esperando_mario"
                    self.vx = 0.0

            # ------------ PISO 0 y 2 → hacia Luigi ------------ #
            else:
                self.vx = -abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                final_x = self.COL_FINAL_LUIGI * 8

                if self.x <= final_x:

                    if luigi.piso != self.piso:
                        juego.fallos += 1
                        juego.invocar_jefe()     # ★ INVOCAR JEFE
                        self._iniciar_caida_fallo()
                        return

                    if self.piso == 0:
                        self.estado = "esperando_luigi"
                        self.vx = 0.0

                    else:
                        self.estado = "entrega"
                        self._tp_sobre_camion()

        # ==========================================================
        #  ESTADO 5 — ESPERANDO A QUE LUIGI SUBA
        # ==========================================================
        elif self.estado == "esperando_luigi":

            if luigi.piso > self.piso:
                self.piso += 1
                self._tp_principio_cinta()
                self.estado = "a_columna"

        # ==========================================================
        #  ESTADO 6 — ESPERANDO A QUE MARIO SUBA
        # ==========================================================
        elif self.estado == "esperando_mario":

            if mario.piso > self.piso:
                self.piso += 1
                self._tp_principio_cinta()
                self.estado = "a_columna"

        # ==========================================================
        #  ESTADO 7 — ENTREGA FINAL
        # ==========================================================
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

    # ---------------- FUNCIONES AUXILIARES ---------------- #

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

    def _iniciar_caida_fallo(self):
        self.estado = "caida_fallo"
        self.vx = 0.0
        self.vy = self.VY_CAIDA

    # ---------------- DIBUJO ---------------- #

    def draw(self):
        if not self.activo:
            return
        pyxel.blt(self.x, self.y, *self.sprite_paquete)
