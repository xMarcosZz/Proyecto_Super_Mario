import pyxel


class Paquete:
    """
    Clase que gestiona el recorrido completo del paquete dentro del almacén.

    El paquete sigue un proceso automatizado:
    - Aparece en el piso 0 (salida).
    - Se desplaza hacia Mario para comprobar si está presente.
    - Recorre la cinta respetando la columna central.
    - Llega a Luigi o Mario según el piso.
    - Sube de piso cuando el personaje correspondiente sube.
    - En el piso 2, se lanza al camión para sumar puntos.
    - Si en algún punto falta el personaje → fallo → caída + aparición del jefe.
    """

    # ==========================================================
    #  CONSTANTES DE POSICIÓN (en tiles, luego se multiplican x8)
    # ==========================================================
    PISOS_Y = [13, 9, 5]  # alturas de los pisos (0, 1, 2)

    # Salida y contacto inicial con Mario
    COL_SALIDA_X = 32
    COL_STOP_MARIO = 26
    COL_MARIO_X = 24

    # Luigi
    COL_LUIGI_X = 6

    # Columna central (punto de teletransporte)
    COL_COL_CONTACTO_DER = 17
    COL_COL_DETRAS_IZQ = 14

    COL_COL_CONTACTO_IZQ = 14
    COL_COL_DETRAS_DER = 17

    # Finales de cinta según piso
    COL_FINAL_LUIGI = 9
    COL_FINAL_MARIO_P1 = 21

    # Posiciones iniciales de cada piso cuando se sube
    POS_INICIO_CINTA = [(22, 13), (10, 9), (22, 5)]

    # Posición del camión donde caerá el paquete
    CAMION_X = 3
    CAMION_Y = 5

    # Velocidades
    VX = 2.5
    VY_CAIDA = 1

    # ==========================================================

    def __init__(self, x, y):
        """
        Inicializa el paquete en una posición dada.
        """
        self.x = x
        self.y = y

        # Posiciones en float para movimiento suave
        self.x_real = float(x)
        self.y_real = float(y)

        # Sprite del paquete
        self.sprite_paquete = (0, 32, 8, 8, 8, 7)

        # Velocidades actuales
        self.vx = -self.VX
        self.vy = 0.0

        # Estado de la máquina
        self.estado = "salida"
        self.piso = 0
        self.activo = True

    # ==========================================================
    #  PROPIEDADES
    # ==========================================================

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

    # ==========================================================
    #  REINICIO DE RECORRIDO
    # ==========================================================

    def reiniciar_salida(self):
        """
        Devuelve el paquete al punto de salida en el piso 0.
        """
        self.estado = "salida"
        self.piso = 0
        self.vx = -self.VX
        self.vy = 0.0

        self.x_real = self.COL_SALIDA_X * 8
        self.y_real = self.PISOS_Y[0] * 8

        self.x = self.x_real
        self.y = self.y_real

    # ==========================================================
    #  UPDATE PRINCIPAL DEL PAQUETE
    # ==========================================================

    def update(self, mario, luigi, juego):
        """
        Actualiza el estado y movimiento del paquete en cada frame.
        Recibe:
            mario, luigi → personajes para comprobar su posición.
            juego → para modificar puntos, fallos y activar al jefe.
        """

        if not self.activo:
            # El paquete está desactivado (muerto tras un fallo)
            return

        # ------------------------------------------------------
        # ESTADO ESPECIAL: CAÍDA POR FALLO
        # ------------------------------------------------------
        if self.estado == "caida_fallo":
            self.y_real += self.vy
            self.y = self.y_real

            # Si sale de pantalla, ver si reaparecer o esperar al jefe
            if self.y > pyxel.height:
                if juego.jefe_timer > 0:
                    self.activo = False  # Se queda muerto hasta que pase el jefe
                else:
                    self.reiniciar_salida()
            return

        # ------------------------------------------------------
        # ESTADO 1 — SALIDA (32 → 26)
        # ------------------------------------------------------
        if self.estado == "salida":
            self._update_salida(mario, juego)
            return

        # ------------------------------------------------------
        # ESTADO 2 — SALIDA DETRÁS DE MARIO
        # ------------------------------------------------------
        if self.estado == "salida_detras_mario":
            self._update_salida_detras_mario(mario, juego)
            return

        # ------------------------------------------------------
        # ESTADO 3 — IR A LA COLUMNA
        # ------------------------------------------------------
        if self.estado == "a_columna":
            self._update_ir_a_columna()
            return

        # ------------------------------------------------------
        # ESTADO 4 — COLUMNA → DESTINO
        # ------------------------------------------------------
        if self.estado == "a_destino":
            self._update_ir_a_destino(mario, luigi, juego)
            return

        # ------------------------------------------------------
        # ESTADO 5 — ESPERANDO A QUE LUIGI SUBA
        # ------------------------------------------------------
        if self.estado == "esperando_luigi":
            if luigi.piso > self.piso:
                self.piso += 1
                self._tp_principio_cinta()
                self.estado = "a_columna"
            return

        # ------------------------------------------------------
        # ESTADO 6 — ESPERANDO A QUE MARIO SUBA
        # ------------------------------------------------------
        if self.estado == "esperando_mario":
            if mario.piso > self.piso:
                self.piso += 1
                self._tp_principio_cinta()
                self.estado = "a_columna"
            return

        # ------------------------------------------------------
        # ESTADO 7 — ENTREGA FINAL
        # ------------------------------------------------------
        if self.estado == "entrega":
            self._update_entrega(juego)
            return

    # ==========================================================
    #  SUBMÉTODOS DE MOVIMIENTO POR ESTADOS
    # ==========================================================

    def _update_salida(self, mario, juego):
        """Movimiento inicial desde 32→26 y comprobación de Mario."""
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
                self._iniciar_caida_fallo()
                return
            self.estado = "salida_detras_mario"

    def _update_salida_detras_mario(self, mario, juego):
        """Movimiento hacia el bloque detrás de Mario."""
        self.vx = -self.VX
        self.x_real += self.vx
        self.x = self.x_real

        x_detras = (self.COL_MARIO_X + 1) * 8

        if self.x <= x_detras:
            if mario.piso != 0:
                juego.fallos += 1
                juego.invocar_jefe()
                self._iniciar_caida_fallo()
                return

            # Teletransporte a la cinta
            self.x_real = 22 * 8
            self.y_real = 13 * 8
            self.x = self.x_real
            self.y = self.y_real

            self.estado = "a_columna"

    def _update_ir_a_columna(self):
        """Movimiento desde la cinta hasta la columna morada."""
        if self.piso == 1:  # Piso 1 va hacia la derecha
            self.vx = abs(self.VX)
            self.x_real += self.vx
            self.x = self.x_real

            if self.x >= self.COL_COL_CONTACTO_IZQ * 8:
                self.x_real = self.COL_COL_DETRAS_DER * 8
                self.x = self.x_real
                self.estado = "a_destino"

        else:  # Pisos 0 y 2 → izquierda
            self.vx = -abs(self.VX)
            self.x_real += self.vx
            self.x = self.x_real

            if self.x <= self.COL_COL_CONTACTO_DER * 8:
                self.x_real = self.COL_COL_DETRAS_IZQ * 8
                self.x = self.x_real
                self.estado = "a_destino"

    def _update_ir_a_destino(self, mario, luigi, juego):
        """Movimiento desde la columna hasta Luigi o Mario según piso."""

        # Piso 1 → Mario
        if self.piso == 1:
            self.vx = abs(self.VX)
            self.x_real += self.vx
            self.x = self.x_real
            final_x = self.COL_FINAL_MARIO_P1 * 8

            if self.x >= final_x:
                if mario.piso != self.piso:
                    juego.fallos += 1
                    juego.invocar_jefe()
                    self._iniciar_caida_fallo()
                    return

                self.estado = "esperando_mario"
                self.vx = 0.0

        # Pisos 0 y 2 → Luigi
        else:
            self.vx = -abs(self.VX)
            self.x_real += self.vx
            self.x = self.x_real
            final_x = self.COL_FINAL_LUIGI * 8

            if self.x <= final_x:
                if luigi.piso != self.piso:
                    juego.fallos += 1
                    juego.invocar_jefe()
                    self._iniciar_caida_fallo()
                    return

                # Piso 0 → esperar a Luigi
                if self.piso == 0:
                    self.estado = "esperando_luigi"
                    self.vx = 0.0

                # Piso 2 → entregar al camión
                else:
                    self.estado = "entrega"
                    self._tp_sobre_camion()

    def _update_entrega(self, juego):
        """Caída del paquete al camión para sumar puntos."""
        self.y_real += self.VY_CAIDA
        self.y = self.y_real

        if self.y >= self.CAMION_Y * 8:
            # Suma de puntos
            juego.puntuacion += 1
            juego.camion.carga += 1

            # Si llena el camión → 10 puntos bonus
            if juego.camion.carga >= 8:
                juego.puntuacion += 10
                juego.camion.carga = 0
                juego.camion.iniciar_reparto()

            self.reiniciar_salida()

    # ==========================================================
    #  FUNCIONES AUXILIARES
    # ==========================================================

    def _tp_principio_cinta(self):
        """Teletransporta el paquete al inicio de la cinta del piso actual."""
        x_tile, y_tile = self.POS_INICIO_CINTA[self.piso]
        self.x_real = x_tile * 8
        self.y_real = y_tile * 8
        self.x = self.x_real
        self.y = self.y_real

    def _tp_sobre_camion(self):
        """Teletransporta el paquete a la posición de caída sobre el camión."""
        self.x_real = self.CAMION_X * 8
        self.y_real = (self.CAMION_Y - 4) * 8
        self.x = self.x_real
        self.y = self.y_real
        self.vy = self.VY_CAIDA

    def _iniciar_caida_fallo(self):
        """Activa el estado de caída cuando el personaje no está presente."""
        self.estado = "caida_fallo"
        self.vx = 0.0
        self.vy = self.VY_CAIDA

    # ==========================================================
    #  DIBUJO
    # ==========================================================

    def draw(self):
        """Dibuja el paquete en pantalla si está activo."""
        if not self.activo:
            return
        pyxel.blt(self.x, self.y, *self.sprite_paquete)
