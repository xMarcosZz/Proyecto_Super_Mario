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
        (10, 9),  # piso 1 → pasa al 2
        (22, 5)  # piso 2 → entrega
    ]

    CAMION_X = 3
    CAMION_Y = 5

    # Velocidades (modificadas por menú)
    VX = 2.5
    VY_CAIDA = 1

    # --------------------------------------------------------------

    def __init__(self, x: int, y: int):
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
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, v):
        self.__x = int(v)

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, v):
        self.__y = int(v)

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
    #   UPDATE PRINCIPAL (MODULARIZADO)
    # --------------------------------------------------

    def update(self, mario, luigi, juego):
        """
        Gestor de estados del paquete. Delega la lógica a métodos privados.
        """
        if not self.activo:
            return

        # Máquina de estados
        if self.estado == "caida_fallo":
            self._update_caida_fallo(juego)

        elif self.estado == "salida":
            self._update_salida(mario, juego)

        elif self.estado == "salida_detras_mario":
            self._update_detras_mario(mario, juego)

        elif self.estado == "a_columna":
            self._update_a_columna()

        elif self.estado == "a_destino":
            self._update_a_destino(mario, luigi, juego)

        elif self.estado == "entrega":
            self._update_entrega(juego)

    # --------------------------------------------------
    #   MÉTODOS PRIVADOS DE LÓGICA (UPDATE)
    # --------------------------------------------------

    def _update_caida_fallo(self, juego):
        """Gestiona la caída libre cuando se ha fallado."""
        self.y_real += self.vy
        self.y = self.y_real

        if self.y > pyxel.height:
            # Si el jefe sigue en pantalla, desactivamos el paquete
            if juego.jefe_timer > 0:
                self.activo = False
            else:
                self.reiniciar_salida()

    def _update_salida(self, mario, juego):
        """Inicio del recorrido en planta baja."""
        self.piso = 0
        self.y_real = self.PISOS_Y[0] * 8
        self.y = self.y_real

        self.vx = -self.VX
        self.x_real += self.vx
        self.x = self.x_real

        # Punto crítico: Mario debe estar en piso 0
        if self.x <= self.COL_STOP_MARIO * 8:
            if mario.piso != 0:
                self._registrar_fallo(juego)
                return

            self.estado = "salida_detras_mario"

    def _update_detras_mario(self, mario, juego):
        """El paquete pasa por detrás de Mario."""
        self.x_real += self.vx
        self.x = self.x_real

        pos_detras = (self.COL_MARIO_X + 1) * 8

        if self.x <= pos_detras:
            if mario.piso != 0:
                self._registrar_fallo(juego)
                return

            # Teletransporte al inicio de la cinta tras Mario
            self.x_real = 22 * 8
            self.y_real = 13 * 8
            self.x = self.x_real
            self.y = self.y_real
            self.estado = "a_columna"

    def _update_a_columna(self):
        """Mueve el paquete hacia la columna central morada."""
        # Piso 1 va a la derecha, Pisos 0 y 2 van a la izquierda
        if self.piso == 1:
            self.vx = abs(self.VX)
            self.x_real += self.vx
            self.x = self.x_real

            if self.x >= self.COL_COL_CONTACTO_IZQ * 8:
                self.x_real = self.COL_COL_DETRAS_DER * 8
                self.x = self.x_real
                self.estado = "a_destino"
        else:
            self.vx = -abs(self.VX)
            self.x_real += self.vx
            self.x = self.x_real

            if self.x <= self.COL_COL_CONTACTO_DER * 8:
                self.x_real = self.COL_COL_DETRAS_IZQ * 8
                self.x = self.x_real
                self.estado = "a_destino"

    def _update_a_destino(self, mario, luigi, juego):
        """Gestiona la llegada al personaje final de cada piso."""

        # --- PISO 1: Entrega a Mario ---
        if self.piso == 1:
            self.vx = abs(self.VX)
            self.x_real += self.vx
            self.x = self.x_real

            if self.x >= self.COL_FINAL_MARIO_P1 * 8:
                if mario.piso != 1:
                    self._registrar_fallo(juego)
                else:
                    self.piso = 2
                    self._tp_principio_cinta()
                    self.estado = "a_columna"

        # --- PISO 0 y 2: Entrega a Luigi ---
        else:
            self.vx = -abs(self.VX)
            self.x_real += self.vx
            self.x = self.x_real

            if self.x <= self.COL_FINAL_LUIGI * 8:
                # Caso Piso 0: Sube al 1
                if self.piso == 0:
                    if luigi.piso != 0:
                        self._registrar_fallo(juego)
                    else:
                        self.piso = 1
                        self._tp_principio_cinta()
                        self.estado = "a_columna"

                # Caso Piso 2: Entrega al camión
                else:
                    if luigi.piso != 2:
                        self._registrar_fallo(juego)
                    else:
                        self.estado = "entrega"
                        self._tp_sobre_camion()

    def _update_entrega(self, juego):
        """Caída final sobre el camión."""
        self.y_real += self.VY_CAIDA
        self.y = self.y_real

        if self.y >= self.CAMION_Y * 8:
            # ÉXITO
            juego.puntuacion += 1
            juego.camion.carga += 1

            # SONIDO DE ENTREGA CORRECTA (Sprint 5)
            # Canal 0, Sonido 0 (definido en Juego.py)
            pyxel.play(0, 0)

            if juego.camion.carga >= 8:
                juego.puntuacion += 10
                juego.camion.carga = 0
                juego.camion.iniciar_reparto()

            self.reiniciar_salida()

    # --------------------------------------------------
    #   AUXILIARES
    # --------------------------------------------------

    def _registrar_fallo(self, juego):
        """Notifica al juego un fallo y cambia estado a caída."""
        juego.fallos += 1
        juego.invocar_jefe()  # Esto ya reproduce el sonido de fallo en Juego.py
        self._fallar()

    def _tp_principio_cinta(self):
        """Teletransporta el paquete al inicio de la cinta del piso actual."""
        x_tile, y_tile = self.POS_INICIO_CINTA[self.piso]
        self.x_real = x_tile * 8
        self.y_real = y_tile * 8
        self.x = self.x_real
        self.y = self.y_real

    def _tp_sobre_camion(self):
        """Coloca el paquete alineado con el camión para caer."""
        self.x_real = self.CAMION_X * 8
        self.y_real = (self.CAMION_Y - 4) * 8
        self.x = self.x_real
        self.y = self.y_real
        self.vy = self.VY_CAIDA

    def _fallar(self):
        """Inicia la física de caída libre."""
        self.estado = "caida_fallo"
        self.vx = 0.0
        self.vy = self.VY_CAIDA

    # --------------------------------------------------
    #   DRAW
    # --------------------------------------------------

    def draw(self):
        if self.activo:
            pyxel.blt(self.x, self.y, *self.sprite_paquete)