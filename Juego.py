import pyxel
import os
# Importamos nuestras propias clases que definen los objetos del juego
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe
from Sonido import GestorSonido
from HUD import HUD


class Juego:
    """
    Clase Principal (El cerebro del programa).

    Esta clase es el 'Director de Orquesta'. Su trabajo es:
    1. Iniciar la ventana y cargar los recursos.
    2. Mantener el bucle infinito del juego (Update y Draw).
    3. Decidir que pantalla se muestra (Menu, Juego, Pausa).
    4. Coordinar la comunicacion entre Mario, Luigi, el Camion y los Paquetes.
    """

    def __init__(self):
        # ESTADOS DEL JUEGO
        # Usamos una cadena de texto para saber en que pantalla estamos.
        # Las opciones son: "menu", "config", "juego", "pausa".
        self.estado = "menu"

        # Bandera para saber si hemos perdido
        self.game_over = False

        # Referencias a los gestores de Sonido y Graficos (HUD).
        # Se inician como None o vacios, y se cargaran luego en ejecutar().
        self.sonido = None
        self.hud = HUD()

        # CONFIGURACION DE DIFICULTAD
        # Lista con las velocidades disponibles para los paquetes
        self.velocidades = [1.5, 2.0, 2.5, 3.0]
        # Textos para mostrar en el menu segun la velocidad
        self.velocidades_texto = ["Muy lenta", "Lenta", "Media", "Rapida"]
        # Indice que apunta a la velocidad seleccionada actualmente (2 = Media)
        self.config_vel_index = 2

        # Indice para saber cuantos paquetes salen (0 = 1 paquete, 1 = 2 paquetes)
        self.config_paquetes_index = 0
        # Variable real que usa el juego para saber cuantos paquetes crear
        self.num_paquetes = 1

        # VARIABLES DE NAVEGACION (CURSORES)
        # Controlan que opcion esta seleccionada en cada menu
        self.menu_opcion = 0
        self.config_cursor = 0
        self.pausa_cursor = 0

        # VARIABLES DE PROGRESO
        self.puntuacion = 0
        self.fallos = 0
        # Cargamos el record desde el archivo de texto al arrancar
        self.record_actual = self.cargar_record()

        # CREACION DE OBJETOS (ENTIDADES)
        # Creamos el camion en la posicion X=8, Y=64 (píxeles)
        self.camion = Camion(8, 64)

        # Creamos a Mario y Luigi en sus posiciones iniciales
        self.mario = Personaje("Mario", 192, 104)
        self.luigi = Personaje("Luigi", 48, 104)

        # Creamos al Jefe (empieza invisible)
        self.jefe = Jefe(120, 24)

        # DEFINICION DE PISOS
        # Lista con la altura Y exacta de cada piso: [Piso 0, Piso 1, Piso 2]
        # Esto sirve para que Mario y Luigi sepan a que altura pintarse.
        pisos_y = [104, 64, 32]
        self.mario.pisos = pisos_y
        self.luigi.pisos = pisos_y

        # Lista vacia donde guardaremos los paquetes activos
        self.paquetes = []

    def ejecutar(self):
        # Esta funcion arranca el motor grafico Pyxel.
        # 1. Definimos el tamaño de la ventana: Ancho 256, Alto 128
        pyxel.init(256, 128, title="Mario Bros")

        # 2. Cargamos las imagenes y sonidos del archivo de recursos
        pyxel.load("recursos.pyxres")

        # 3. Inicializamos el sistema de sonido ahora que Pyxel esta listo
        self.sonido = GestorSonido()

        # 4. Arrancamos el bucle infinito.
        # Pyxel llamara a self.update() y self.draw() 30 veces por segundo.
        pyxel.run(self.update, self.draw)

    def cargar_record(self):
        # Intenta leer el archivo 'record.txt' del disco duro.
        # Si el archivo existe, lee el numero y lo devuelve.
        if os.path.exists("record.txt"):
            try:
                archivo = open("record.txt", "r")
                contenido = archivo.read()
                valor = int(contenido)
                archivo.close()
                return valor
            except:
                # Si el archivo esta corrupto o vacio, devolvemos 0
                return 0
        # Si el archivo no existe, el record es 0
        return 0

    def guardar_record(self):
        # Solo guardamos si la puntuacion actual supera al record guardado
        if self.puntuacion > self.record_actual:
            self.record_actual = self.puntuacion
            try:
                # Abrimos el archivo en modo escritura ("w")
                archivo = open("record.txt", "w")
                archivo.write(str(self.record_actual))
                archivo.close()
            except:
                # Si falla (por ejemplo por permisos), no hacemos nada
                pass

    def update(self):
        # ESTA ES LA FUNCION PRINCIPAL DE LOGICA
        # Funciona como un distribuidor de trafico.
        # Dependiendo del valor de 'self.estado', ejecuta un codigo u otro.

        if self.estado == "menu":
            # Si estamos en el menu, permitimos salir con Escape
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()
            self._update_menu()

        elif self.estado == "config":
            # Si estamos en config, Escape nos devuelve al menu
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                self.estado = "menu"
            self._update_config()

        elif self.estado == "juego":
            # DETECCION DE PAUSA
            # Comprobamos si el jugador pulsa P o Escape
            tecla_pausa = pyxel.btnp(pyxel.KEY_P)
            tecla_escape = pyxel.btnp(pyxel.KEY_ESCAPE)

            if tecla_pausa or tecla_escape:
                # Cambiamos el estado a pausa
                self.estado = "pausa"
                self.pausa_cursor = 0
                # Paramos la musica para dar sensacion de pausa
                self.sonido.detener_musica()
            else:
                # Si no hay pausa, ejecutamos la logica del juego normal
                self._update_juego()

        elif self.estado == "pausa":
            # Ejecutamos la logica del menu de pausa
            self._update_pausa()

    def _update_menu(self):
        # LOGICA DEL MENU PRINCIPAL

        # Mover cursor arriba
        if pyxel.btnp(pyxel.KEY_UP):
            # Restamos 1 y usamos modulo 2 para rotar entre 0 y 1
            self.menu_opcion = (self.menu_opcion - 1) % 2

        # Mover cursor abajo
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_opcion = (self.menu_opcion + 1) % 2

        # Seleccionar opcion con Enter
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_opcion == 0:
                self.estado = "config"  # Ir a configuracion
            else:
                pyxel.quit()  # Salir del juego

    def _update_config(self):
        # LOGICA DEL MENU DE CONFIGURACION

        # Mover cursor verticalmente (4 opciones)
        if pyxel.btnp(pyxel.KEY_UP):
            self.config_cursor = (self.config_cursor - 1) % 4

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.config_cursor = (self.config_cursor + 1) % 4

        # Modificar valores con Izquierda/Derecha

        # Caso 1: Estamos sobre la opcion "Velocidad"
        if self.config_cursor == 0:
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.config_vel_index = (self.config_vel_index - 1) % 4
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_vel_index = (self.config_vel_index + 1) % 4

        # Caso 2: Estamos sobre la opcion "Paquetes"
        elif self.config_cursor == 1:
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                # Cambiamos entre 0 y 1
                self.config_paquetes_index = 1 - self.config_paquetes_index

        # Confirmar seleccion con Enter
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.config_cursor == 2:
                # Opcion "EMPEZAR PARTIDA"
                self.iniciar_partida()
            elif self.config_cursor == 3:
                # Opcion "VOLVER"
                self.estado = "menu"
                self.sonido.detener_musica()

    def _update_pausa(self):
        # LOGICA DEL MENU DE PAUSA (Ventana flotante)

        if pyxel.btnp(pyxel.KEY_UP):
            self.pausa_cursor = (self.pausa_cursor - 1) % 2

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.pausa_cursor = (self.pausa_cursor + 1) % 2

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.pausa_cursor == 0:
                # CONTINUAR: Volvemos al juego y reactivamos musica
                self.estado = "juego"
                self.sonido.reproducir_musica_juego()
            else:
                # SALIR: Volvemos al menu principal
                self.estado = "menu"
                self.sonido.detener_musica()

        # Tecla rapida para quitar pausa
        tecla_pausa = pyxel.btnp(pyxel.KEY_P)
        tecla_escape = pyxel.btnp(pyxel.KEY_ESCAPE)

        if tecla_pausa or tecla_escape:
            self.estado = "juego"
            self.sonido.reproducir_musica_juego()

    def iniciar_partida(self):
        # ESTA FUNCION RESETEA TODO PARA EMPEZAR DE CERO
        # Es importante para que no queden datos de la partida anterior.

        self.puntuacion = 0
        self.fallos = 0
        self.game_over = False
        # Recargamos el record por si se actualizo
        self.record_actual = self.cargar_record()

        # Reseteo del camion
        self.camion.carga = 0
        self.camion.estado = Camion.PARADO
        self.camion.x = 8
        self.camion.reparto_terminado = False

        # Reseteo del Jefe
        self.jefe.desaparecer()
        self.jefe_timer = 0
        self.shake = 0

        # Reseteo de posicion de personajes
        self.mario.piso = 0
        self.luigi.piso = 0
        self.mario.y = self.mario.pisos[0]
        self.luigi.y = self.luigi.pisos[0]

        # APLICAMOS LA CONFIGURACION ELEGIDA EN EL MENU
        # Velocidad del paquete
        Paquete.VX = self.velocidades[self.config_vel_index]

        # Numero de paquetes
        if self.config_paquetes_index == 0:
            self.num_paquetes = 1
        else:
            self.num_paquetes = 2

        # Limpiamos la lista y creamos los paquetes nuevos
        self.paquetes = []

        # Paquete 1: Se crea activo y listo para salir
        p1 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
        p1.reiniciar_salida()
        self.paquetes.append(p1)

        # Paquete 2: Si esta configurado, se crea pero INACTIVO (dormido)
        # Se despertara luego segun la logica de distancia
        if self.num_paquetes == 2:
            p2 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
            p2.reiniciar_salida()
            p2.activo = False
            self.paquetes.append(p2)

        # Cambiamos estado y arrancamos musica
        self.estado = "juego"
        self.sonido.reproducir_musica_juego()

    def _update_juego(self):
        # LOGICA DURANTE LA PARTIDA
        # Este metodo gestiona las prioridades de lo que ocurre en pantalla.

        # PRIORIDAD 1: GAME OVER
        # Si hemos perdido, el juego se congela y espera una tecla.
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.iniciar_partida()
            elif pyxel.btnp(pyxel.KEY_M):
                self.estado = "menu"
                self.sonido.detener_musica()
            return

        # PRIORIDAD 2: JEFE REGAÑANDO (FALLO)
        # Si el jefe esta activo, el juego se pausa temporalmente.
        if self.jefe_timer > 0:
            self.jefe_timer = self.jefe_timer - 1
            self.jefe.update()

            # Solo actualizamos los paquetes que esten cayendo al vacio
            # para que se vea la animacion de caida.
            for p in self.paquetes:
                if p.estado == "caida_fallo":
                    p.update(self.mario, self.luigi, self)

            # Activamos el temblor de pantalla
            self.shake = 3

            # CUANDO TERMINA EL JEFE (Timer llega a 0)
            if self.jefe_timer <= 0:
                self.jefe.desaparecer()
                self.shake = 0

                # Reseteamos los paquetes para seguir jugando

                # Paquete 1: Lo reseteamos y lo activamos inmediatamente
                if len(self.paquetes) > 0:
                    self.paquetes[0].reiniciar_salida()
                    self.paquetes[0].activo = True

                # Paquete 2: Lo reseteamos pero lo dejamos DORMIDO
                # Asi evitamos que salgan los dos a la vez despues de un fallo
                if len(self.paquetes) > 1:
                    self.paquetes[1].reiniciar_salida()
                    self.paquetes[1].activo = False

            # Si esta el jefe, no hacemos nada mas en este frame
            return

        # PRIORIDAD 3: CAMION REPARTIENDO
        self.camion.update()

        # Si el camion no esta en estado PARADO, significa que esta fuera.
        # En este caso, "congelamos" la fabrica (return).
        if self.camion.estado != Camion.PARADO:
            if self.camion.reparto_terminado:
                self.camion.reparto_terminado = False
            return

        # PRIORIDAD 4: JUEGO NORMAL (Fabrica funcionando)

        # Controles de los personajes
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover_abajo()
        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover_abajo()

        # LOGICA AVANZADA DE 2 PAQUETES
        # Controlamos cuando debe salir el segundo paquete para que no se solapen.
        if self.num_paquetes == 2:
            p1 = self.paquetes[0]
            p2 = self.paquetes[1]

            # Calculamos si el primer paquete esta lejos del inicio (18 bloques)
            limite_distancia = 18 * 8
            esta_lejos = p1.x < limite_distancia

            # O si el primer paquete ya ha cambiado de piso
            cambio_piso = p1.piso > 0

            # Si el paquete 2 esta dormido Y (el 1 esta lejos O en otro piso)
            if p2.activo == False:
                if p1.activo == True:
                    if esta_lejos or cambio_piso:
                        # Despertamos al paquete 2
                        p2.reiniciar_salida()
                        p2.activo = True

        # Actualizamos la logica de movimiento de todos los paquetes activos
        for p in self.paquetes:
            p.update(self.mario, self.luigi, self)

        # COMPROBACION DE GAME OVER
        if self.fallos >= 3:
            self.game_over = True
            self.guardar_record()
            self.sonido.sfx_game_over()

    def invocar_jefe(self):
        # Esta funcion la llama un Paquete cuando detecta que se cae.
        self.jefe.aparecer()
        self.jefe_timer = 120  # El jefe estara 120 frames (4 segundos)
        self.shake = 3
        self.sonido.sfx_fallo()

    def draw(self):
        # DISTRIBUIDOR DE DIBUJADO
        # Delega el trabajo de pintar al objeto HUD

        if self.estado == "menu":
            self.hud.draw_menu(self.menu_opcion)

        elif self.estado == "config":
            vt = self.velocidades_texto[self.config_vel_index]

            if self.config_paquetes_index == 0:
                n = 1
            else:
                n = 2

            self.hud.draw_config(self.config_cursor, vt, n)

        elif self.estado == "juego":
            self._draw_juego()

        elif self.estado == "pausa":
            # En pausa, dibujamos el juego de fondo congelado
            self._draw_juego()
            # Y encima dibujamos la ventana de pausa
            self.hud.draw_pausa(self.pausa_cursor, self.puntuacion)

    def _draw_juego(self):
        # DIBUJADO DE LA PARTIDA

        # Limpiamos pantalla
        pyxel.cls(7)

        # Calculo del temblor (Shake) si el jefe esta enfadado
        dx = 0
        dy = 0

        if self.jefe_timer > 0:
            dx = pyxel.rndi(-3, 3)
            dy = pyxel.rndi(-3, 3)

        # 1. Dibujamos el fondo (Tilemap) aplicando el temblor
        pyxel.bltm(dx, dy, 0, 0, 0, pyxel.width, pyxel.height, colkey=7)

        # 2. Dibujamos las entidades
        self.camion.draw()
        self.mario.draw()
        self.luigi.draw()

        # 3. Dibujamos los paquetes
        for p in self.paquetes:
            p.draw()

        # 4. Dibujamos al jefe
        self.jefe.draw()

        # 5. Dibujamos el marcador (HUD)
        self.hud.draw_marcador_juego(self.puntuacion, self.record_actual, self.fallos, self.camion.carga)

        # 6. Mensajes especiales
        if self.camion.estado == Camion.FUERA:
            self.hud.draw_mensaje_reparto()

        if self.game_over:
            # Comprobamos si es un nuevo record para mostrar mensaje especial
            nuevo = False
            if self.puntuacion >= self.record_actual:
                if self.puntuacion > 0:
                    nuevo = True

            self.hud.draw_game_over(self.puntuacion, self.record_actual, nuevo)