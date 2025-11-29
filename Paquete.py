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
    # Altura de las cintas (y)
    PISOS_Y = [13, 9, 5]  # piso 0, 1, 2

    # Salida y primer chequeo con Mario (piso 0)
    COL_SALIDA_X = 32      # donde aparece inicialmente
    COL_STOP_MARIO = 26    # primer punto de comprobación con Mario
    COL_MARIO_X = 24       # columna de Mario (para ir "detrás")

    # Luigi (columna de referencia, solo para saber en qué piso está)
    COL_LUIGI_X = 6

    # Columna morada central
    COL_COL_CONTACTO_DER = 17  # punto de contacto viniendo desde la derecha
    COL_COL_DETRAS_IZQ = 14    # posición detrás viniendo desde la derecha

    COL_COL_CONTACTO_IZQ = 14  # punto de contacto viniendo desde la izquierda
    COL_COL_DETRAS_DER = 17    # posición detrás viniendo desde la izquierda

    # Final de cinta lado Luigi (piso 0 y 2)
    COL_FINAL_LUIGI = 9

    # Final de cinta lado Mario (piso 1)
    COL_FINAL_MARIO_P1 = 21

    # Posiciones iniciales de las cintas cuando se sube de piso
    #   piso 0 -> (22,13)
    #   piso 1 -> (10, 9)
    #   piso 2 -> (22, 5)
    POS_INICIO_CINTA = [(22, 13), (10, 9), (22, 5)]

    # Camión
    CAMION_X = 3   # donde aparecerá antes de caer
    CAMION_Y = 5   # y en tiles

    # Velocidades
    VX = 2.5
    VY_CAIDA = 1

    def __init__(self, x, y):
        # Posición en píxeles
        self.x = x
        self.y = y

        self.x_real = float(x)
        self.y_real = float(y)

        self.sprite_paquete = (0, 32, 8, 8, 8, 7)

        # Velocidades
        self.vx = -self.VX
        self.vy = 0.0

        # Estado de la máquina
        # "salida"             : 32 → 26 (comprobar Mario piso0)
        # "salida_detras_mario": 26 → detrás de Mario
        # "a_columna"          : tramo hasta la columna
        # "a_destino"          : columna → lado de Luigi / Mario según piso
        # "esperando_luigi"    : parado en piso 0 esperando que Luigi suba
        # "esperando_mario"    : parado en piso 1 esperando que Mario suba
        # "entrega"            : cayendo sobre el camión (punto)
        # "caida_fallo"        : caída cuando falla (no hay personaje)
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
        """Vuelve a colocar el paquete en la salida (piso 0)."""
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
        #  ESTADO: CAÍDA POR FALLO (SIN PERSONAJE)
        # ==========================================================
        if self.estado == "caida_fallo":
            self.y_real += self.vy
            self.y = self.y_real
            if self.y > pyxel.height:
                # cuando desaparece, vuelve a la salida
                self.reiniciar_salida()
            return

        # ==========================================================
        #  ESTADO 1 — SALIDA: 32,13 → 26,13 (solo piso 0)
        # ==========================================================
        if self.estado == "salida":

            self.piso = 0
            self.y_real = self.PISOS_Y[0] * 8
            self.y = self.y_real

            self.vx = -self.VX
            self.x_real += self.vx
            self.x = self.x_real

            # 32 → 26
            if self.x <= self.COL_STOP_MARIO * 8:

                # ¿Mario está en el piso 0?
                if mario.piso != 0:
                    juego.fallos += 1
                    self._iniciar_caida_fallo()
                    return

                # Continuar moviéndose hasta llegar detrás de Mario
                self.estado = "salida_detras_mario"

        # ==========================================================
        #  ESTADO 2 — SALIDA DETRÁS DE MARIO: 26 → detrás de Mario
        # ==========================================================
        elif self.estado == "salida_detras_mario":

            self.vx = -self.VX
            self.x_real += self.vx
            self.x = self.x_real

            x_detras_mario = (self.COL_MARIO_X + 1) * 8  # bloque 25

            # ¿ha llegado detrás de Mario?
            if self.x <= x_detras_mario:

                # ¿Mario sigue en el piso 0? si no → fallo
                if mario.piso != 0:
                    juego.fallos += 1
                    self._iniciar_caida_fallo()
                    return

                # TELETRANSPORTE A LA CINTA (22,13)
                self.x_real = 22 * 8
                self.y_real = 13 * 8
                self.x = self.x_real
                self.y = self.y_real

                # continuar por la cinta
                self.estado = "a_columna"
                self.vx = -self.VX

        # ==========================================================
        #  ESTADO 3 — DE LA CINTA A LA COLUMNA (según piso)
        # ==========================================================
        elif self.estado == "a_columna":

            # Piso 1: movimiento hacia la DERECHA (10 → 14)
            if self.piso == 1:
                self.vx = abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                if self.x >= self.COL_COL_CONTACTO_IZQ * 8:
                    # Teletransporte al otro lado (17,9)
                    self.x_real = self.COL_COL_DETRAS_DER * 8
                    self.x = self.x_real
                    self.estado = "a_destino"

            # Pisos 0 y 2: movimiento hacia la IZQUIERDA (22 → 17)
            else:
                self.vx = -abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                if self.x <= self.COL_COL_CONTACTO_DER * 8:
                    # Teletransporte al otro lado (14,y)
                    self.x_real = self.COL_COL_DETRAS_IZQ * 8
                    self.x = self.x_real
                    self.estado = "a_destino"

        # ==========================================================
        #  ESTADO 4 — COLUMNA → DESTINO (Luigi o Mario según piso)
        # ==========================================================
        elif self.estado == "a_destino":

            # ---------- PISO 1: hacia la derecha hasta Mario (21,9) ----------
            if self.piso == 1:
                self.vx = abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                final_x = self.COL_FINAL_MARIO_P1 * 8  # 21,9

                if self.x >= final_x:
                    # ¿Mario está en este piso?
                    if mario.piso != self.piso:
                        juego.fallos += 1
                        self._iniciar_caida_fallo()
                        return

                    # Se queda esperando a que Mario suba al último piso
                    self.estado = "esperando_mario"
                    self.vx = 0.0

            # ---------- PISOS 0 y 2: hacia la izquierda hasta Luigi (9,y) ----------
            else:
                self.vx = -abs(self.VX)
                self.x_real += self.vx
                self.x = self.x_real

                final_x = self.COL_FINAL_LUIGI * 8  # 9

                if self.x <= final_x:

                    # PISO 0: Luigi debe estar para subir con la caja
                    if self.piso == 0:
                        if luigi.piso != self.piso:
                            juego.fallos += 1
                            self._iniciar_caida_fallo()
                            return

                        self.estado = "esperando_luigi"
                        self.vx = 0.0

                    # PISO 2: Luigi la tira al camión
                    else:  # piso 2
                        if luigi.piso != self.piso:
                            juego.fallos += 1
                            self._iniciar_caida_fallo()
                            return

                        self.estado = "entrega"
                        self._tp_sobre_camion()

        # ==========================================================
        #  ESTADO 5 — ESPERANDO A QUE LUIGI SUBA (piso 0)
        # ==========================================================
        elif self.estado == "esperando_luigi":
            # Cuando Luigi suba de piso, la caja sube a la cinta del piso 1
            if luigi.piso > self.piso:
                self.piso += 1
                self._tp_principio_cinta()
                self.estado = "a_columna"
                # la dirección se ajustará en a_columna según el piso

        # ==========================================================
        #  ESTADO 6 — ESPERANDO A QUE MARIO SUBA (piso 1)
        # ==========================================================
        elif self.estado == "esperando_mario":
            # Cuando Mario suba de piso, la caja sube a la cinta del piso 2
            if mario.piso > self.piso:
                self.piso += 1
                self._tp_principio_cinta()
                self.estado = "a_columna"

        # ==========================================================
        #  ESTADO 7 — ENTREGA FINAL (caída sobre el camión)
        # ==========================================================
        elif self.estado == "entrega":
            self.y_real += self.VY_CAIDA
            self.y = self.y_real

            # Cuando llega a la altura del camión se considera entregado
            if self.y >= self.CAMION_Y * 8:
                # 1 punto por paquete
                juego.puntuacion += 1

                # Aumentar la carga del camión
                juego.camion.carga += 1

                # Si ya hay 8 paquetes entregados, +10 puntos extra
                if juego.camion.carga >= 8:
                    juego.puntuacion += 10
                    juego.camion.carga = 0
                    juego.camion.iniciar_reparto()  # ← ESTA LÍNEA FALTABA

                # Reiniciar el recorrido del paquete
                self.reiniciar_salida()

    # ---------------- FUNCIONES AUXILIARES ---------------- #

    def _tp_principio_cinta(self):
        """
        Teletransporta el paquete al principio de la cinta
        del piso actual (cuando se sube de piso).
        """
        x_tile, y_tile = self.POS_INICIO_CINTA[self.piso]
        self.x_real = x_tile * 8
        self.y_real = y_tile * 8
        self.x = self.x_real
        self.y = self.y_real

    def _tp_sobre_camion(self):
        """Teletransporta el paquete encima del camión (para la caída final)."""
        self.x_real = self.CAMION_X * 8
        # 3–4 bloques por encima del camión
        self.y_real = (self.CAMION_Y - 4) * 8
        self.x = self.x_real
        self.y = self.y_real
        self.vy = self.VY_CAIDA

    def _iniciar_caida_fallo(self):
        """Empieza la animación de caída cuando se produce un fallo."""
        self.estado = "caida_fallo"
        self.vx = 0.0
        self.vy = self.VY_CAIDA

    # ---------------- DIBUJO ---------------- #

    def draw(self):
        if not self.activo:
            return
        pyxel.blt(self.x, self.y, *self.sprite_paquete)
