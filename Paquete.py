import pyxel


class Paquete:
    """
    Clase Paquete
    -------------
    Representa una caja o botella que debe viajar por la fábrica.

    PATRÓN DE DISEÑO: MÁQUINA DE ESTADOS
    En lugar de usar un solo método gigante con muchos 'if', el paquete tiene
    un atributo 'self.estado' que indica qué está haciendo en ese momento:
    1. "salida": Saliendo de la máquina inicial.
    2. "a_columna": Viajando hacia la estructura central.
    3. "a_destino": Viajando hacia el personaje (Mario/Luigi).
    4. "entrega": Cayendo hacia el camión.
    5. "caida_fallo": Cayendo al vacío por un error.
    """

    # Coordenadas Y (altura en píxeles) de los 3 pisos (0, 1, 2)
    # Piso 0 = 13 tiles, Piso 1 = 9 tiles, Piso 2 = 5 tiles
    PISOS_Y = [13, 9, 5]

    # --- Columnas (Coordenadas X en tiles) para lógica de movimiento ---

    # Dónde nace el paquete
    COL_SALIDA_X = 32

    # Dónde debe estar Mario para recoger el primer paquete
    COL_STOP_MARIO = 26

    # Posiciones de los personajes
    COL_MARIO_X = 24
    COL_LUIGI_X = 6

    # Puntos de contacto con la columna central (estructura morada)
    # Sirven para detectar cuándo el paquete toca el centro para "teletransportarse"
    COL_COL_CONTACTO_DER = 17  # Viniendo desde la derecha
    COL_COL_CONTACTO_IZQ = 14  # Viniendo desde la izquierda

    # Puntos de aparición tras cruzar la columna central
    COL_COL_DETRAS_IZQ = 14
    COL_COL_DETRAS_DER = 17

    # Límites donde el personaje debe recoger el paquete antes de que caiga
    COL_FINAL_LUIGI = 9
    COL_FINAL_MARIO_P1 = 21

    # Coordenadas (Tile X, Tile Y) donde reaparece el paquete al subir de piso
    # Esto simula que el personaje lo ha subido a la cinta superior
    POS_INICIO_CINTA = [
        (22, 13),  # Inicio Piso 0
        (10, 9),  # Inicio Piso 1
        (22, 5)  # Inicio Piso 2
    ]

    # Posición del camión para la entrega final
    CAMION_X = 3
    CAMION_Y = 5

    # Velocidad horizontal base (se modificará desde el menú de opciones)
    VX = 2.5
    # Velocidad de caída vertical (gravedad)
    VY_CAIDA = 1


    def __init__(self, x: int, y: int):
        """
        Inicializa un nuevo paquete en la posición (x, y).
        """
        self.x = x
        self.y = y

        # Usamos variables float (reales) para calcular el movimiento suave.
        # Si usáramos solo int, el movimiento sería a saltos bruscos.
        self.x_real = float(x)
        self.y_real = float(y)

        # Definición del sprite en el banco de imágenes:
        # (banco 0, u=32, v=8, ancho=8, alto=8, color_transparente=7)
        self.sprite_paquete = (0, 32, 8, 8, 8, 7)

        # Velocidad actual
        self.vx = -self.VX  # Empieza moviéndose a la izquierda
        self.vy = 0.0

        # Estado inicial
        self.estado = "salida"
        self.piso = 0
        self.activo = True  # Si False, no se actualiza ni dibuja


    # PROPIEDADES (GETTERS / SETTERS)

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



    def reiniciar_salida(self):
        """
        Resetea el paquete a su posición inicial (arriba a la derecha).
        Se usa cuando el paquete ha sido entregado o se ha caído.
        """
        self.estado = "salida"
        self.piso = 0
        self.vx = -self.VX
        self.vy = 0.0

        # Posición inicial en píxeles (Tile * 8)
        self.x_real = self.COL_SALIDA_X * 8
        self.y_real = self.PISOS_Y[0] * 8

        # Sincronizamos las coordenadas enteras
        self.x = self.x_real
        self.y = self.y_real

        self.activo = True

    def update(self, mario, luigi, juego):
        """
        MÉTODO PRINCIPAL DE INTELIGENCIA (UPDATE)
        -----------------------------------------
        Actúa como un 'distribuidor' de tráfico. Dependiendo del 'self.estado',
        llama a una función diferente para gestionar el comportamiento.

        Recibe:
            - mario, luigi: Para comprobar si están en el sitio correcto.
            - juego: Para sumar puntos, registrar fallos o llamar al sonido.
        """
        if self.activo == False:
            return

        # --- MÁQUINA DE ESTADOS ---
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


    # LÓGICA ESPECÍFICA POR ESTADO (MÉTODOS PRIVADOS)


    def _update_caida_fallo(self, juego):
        """Comportamiento: El paquete cae al vacío tras un error."""
        self.y_real = self.y_real + self.vy
        self.y = self.y_real

        # Si el paquete sale por la parte inferior de la pantalla
        if self.y > pyxel.height:
            # Si el jefe todavía está regañando, esperamos
            if juego.jefe_timer > 0:
                self.activo = False
            else:
                # Si ya terminó el jefe, reiniciamos el paquete arriba
                self.reiniciar_salida()

    def _update_salida(self, mario, juego):
        """Comportamiento: Sale de la máquina y va hacia Mario (Piso 0)."""
        self.piso = 0
        self.y_real = self.PISOS_Y[0] * 8
        self.y = self.y_real

        # Movimiento hacia la izquierda
        self.vx = -self.VX
        self.x_real = self.x_real + self.vx
        self.x = self.x_real

        # Límite donde Mario debe recogerlo
        limite = self.COL_STOP_MARIO * 8

        # Si cruzamos el límite...
        if self.x <= limite:
            # VERIFICACIÓN: ¿Está Mario en el piso 0?
            if mario.piso != 0:
                # NO ESTÁ -> Fallo
                self._registrar_fallo(juego)
            else:
                # SÍ ESTÁ -> El paquete pasa "detrás" de él visualmente
                self.estado = "salida_detras_mario"

    def _update_detras_mario(self, mario, juego):
        """Comportamiento: Efecto visual de cruzar tras Mario."""
        self.x_real = self.x_real + self.vx
        self.x = self.x_real

        pos_detras = (self.COL_MARIO_X + 1) * 8

        # Cuando termina de pasar a Mario...
        if self.x <= pos_detras:
            # Doble chequeo por seguridad
            if mario.piso != 0:
                self._registrar_fallo(juego)
            else:
                # TELETRANSPORTE: Lo enviamos al inicio de la cinta central
                self.x_real = 22 * 8
                self.y_real = 13 * 8
                self.x = self.x_real
                self.y = self.y_real
                # Cambiamos estado para que viaje hacia el centro
                self.estado = "a_columna"

    def _update_a_columna(self):
        """Comportamiento: Viaja hacia la estructura central morada."""

        # Si está en Piso 1, va hacia la Derecha (Mario)
        if self.piso == 1:
            self.vx = abs(self.VX)  # Velocidad positiva
            self.x_real = self.x_real + self.vx
            self.x = self.x_real

            # Si toca la columna central...
            limite = self.COL_COL_CONTACTO_IZQ * 8
            if self.x >= limite:
                # Teletransporte al otro lado de la columna
                self.x_real = self.COL_COL_DETRAS_DER * 8
                self.x = self.x_real
                self.estado = "a_destino"

        # Si está en Piso 0 o 2, va hacia la Izquierda (Luigi)
        else:
            self.vx = -abs(self.VX)  # Velocidad negativa
            self.x_real = self.x_real + self.vx
            self.x = self.x_real

            # Si toca la columna central...
            limite = self.COL_COL_CONTACTO_DER * 8
            if self.x <= limite:
                # Teletransporte al otro lado
                self.x_real = self.COL_COL_DETRAS_IZQ * 8
                self.x = self.x_real
                self.estado = "a_destino"

    def _update_a_destino(self, mario, luigi, juego):
        """Comportamiento: Viaja desde el centro hacia el personaje receptor."""

        # --- CASO PISO 1: El paquete va hacia la derecha (MARIO) ---
        if self.piso == 1:
            self.vx = abs(self.VX)
            self.x_real = self.x_real + self.vx
            self.x = self.x_real

            limite = self.COL_FINAL_MARIO_P1 * 8

            # Si llega al borde...
            if self.x >= limite:
                # ¿Está Mario en el piso 1?
                if mario.piso != 1:
                    self._registrar_fallo(juego)
                else:
                    # ÉXITO: Mario lo coge y lo sube al Piso 2
                    self.piso = 2
                    self._tp_principio_cinta()  # Teletransporte al inicio cinta
                    self.estado = "a_columna"  # Reinicia ciclo viaje

        # --- CASO PISOS 0 y 2: El paquete va hacia la izquierda (LUIGI) ---
        else:
            self.vx = -abs(self.VX)
            self.x_real = self.x_real + self.vx
            self.x = self.x_real

            limite = self.COL_FINAL_LUIGI * 8

            # Si llega al borde...
            if self.x <= limite:

                # Subcaso: Estamos en el Piso 0
                if self.piso == 0:
                    # ¿Está Luigi en el piso 0?
                    if luigi.piso != 0:
                        self._registrar_fallo(juego)
                    else:
                        # ÉXITO: Luigi lo coge y lo sube al Piso 1
                        self.piso = 1
                        self._tp_principio_cinta()
                        self.estado = "a_columna"

                # Subcaso: Estamos en el Piso 2 (Final)
                else:
                    # ¿Está Luigi en el piso 2?
                    if luigi.piso != 2:
                        self._registrar_fallo(juego)
                    else:
                        # ÉXITO TOTAL: Luigi lo tira al camión
                        self.estado = "entrega"
                        self._tp_sobre_camion()

    def _update_entrega(self, juego):
        """Comportamiento: Caída libre controlada hacia el camión."""
        # Aplicamos gravedad
        self.y_real = self.y_real + self.VY_CAIDA
        self.y = self.y_real

        # Si toca el camión...
        if self.y >= self.CAMION_Y * 8:
            # 1. Sumamos Puntos
            juego.puntuacion = juego.puntuacion + 1
            juego.camion.carga = juego.camion.carga + 1

            # 2. Reproducimos sonido
            juego.sonido.sfx_entrega()

            # 3. Comprobamos si el camión está lleno (8 paquetes)
            if juego.camion.carga >= 8:
                juego.puntuacion = juego.puntuacion + 10
                juego.camion.carga = 0
                juego.camion.iniciar_reparto()  # El camión se va

            # 4. El paquete ha cumplido su misión, vuelve a salir
            self.reiniciar_salida()


    # MÉTODOS AUXILIARES


    def _registrar_fallo(self, juego):
        """Gestiona las consecuencias de un fallo."""
        juego.fallos = juego.fallos + 1
        juego.invocar_jefe()  # Llama al jefe y reproduce sonido error
        self._fallar()  # Inicia la física de caída

    def _tp_principio_cinta(self):
        """Coloca el paquete visualmente al inicio de la cinta del piso actual."""
        pos = self.POS_INICIO_CINTA[self.piso]
        x_tile = pos[0]
        y_tile = pos[1]

        self.x_real = x_tile * 8
        self.y_real = y_tile * 8
        self.x = self.x_real
        self.y = self.y_real

    def _tp_sobre_camion(self):
        """Coloca el paquete alineado con el camión listo para caer."""
        self.x_real = self.CAMION_X * 8
        self.y_real = (self.CAMION_Y - 4) * 8
        self.x = self.x_real
        self.y = self.y_real
        self.vy = self.VY_CAIDA

    def _fallar(self):
        """Cambia el estado a caída libre (Game Over para este paquete)."""
        self.estado = "caida_fallo"
        self.vx = 0.0
        self.vy = self.VY_CAIDA

    def draw(self):
        """Dibuja el paquete si está activo."""
        if self.activo:
            pyxel.blt(self.x, self.y, *self.sprite_paquete)