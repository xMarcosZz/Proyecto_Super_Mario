"""
Juego.py
--------
Módulo principal del proyecto.
Responsabilidad: Coordinar el bucle de juego (Init, Update, Draw) y gestionar
la comunicación entre las entidades (Personajes, Paquetes, HUD, Sonido).
"""
import pyxel
import os
from Camion import Camion
from Personaje import Personaje
from Paquete import Paquete
from Jefe import Jefe
from Sonido import GestorSonido
from HUD import HUD


class Juego:
    """
    Clase Principal (Main Controller).
    Contiene la instancia de Pyxel y los objetos del juego.
    """

    def __init__(self):
        """
        Constructor: Inicializa las variables lógicas.
        NOTA: Aquí NO iniciamos la ventana de Pyxel todavía, solo los datos.
        """
        # Estado actual de la aplicación.
        # Posibles: "menu", "config", "juego", "pausa"
        self.estado = "menu"
        self.game_over = False

        # Referencias a los gestores auxiliares (se crearán en ejecutar())
        self.sonido = None
        self.hud = HUD()

        # --- Variables de Configuración ---
        self.velocidades = [1.5, 2.0, 2.5, 3.0]
        self.velocidades_texto = ["Muy lenta", "Lenta", "Media", "Rápida"]
        self.config_vel_index = 2 # Por defecto velocidad media

        self.config_paquetes_index = 0 # 0 = 1 paquete, 1 = 2 paquetes
        self.num_paquetes = 1

        # Variables de navegación por menús
        self.menu_opcion = 0   # Índice del menú principal
        self.config_cursor = 0 # Índice del menú configuración

        # NUEVO: Cursor para el menú de pausa
        self.pausa_cursor = 0

        # Marcadores de partida
        self.puntuacion = 0
        self.fallos = 0
        self.record_actual = self.cargar_record()

        # --- Instanciación de Objetos (Entidades) ---
        # Posicionamos los objetos multiplicando Tiles * 8 para obtener Píxeles
        self.camion = Camion(1 * 8, 8 * 8)
        self.mario = Personaje("Mario", 24 * 8, 13 * 8)
        self.luigi = Personaje("Luigi", 6 * 8, 13 * 8)
        self.jefe = Jefe(15 * 8, 3 * 8)

        # Definimos las alturas de los pisos y se las pasamos a los personajes
        self.pisos = [13 * 8, 8 * 8, 4 * 8]
        self.mario.pisos = self.pisos
        self.luigi.pisos = self.pisos

        # Lista vacía para los paquetes (se llenará al empezar partida)
        self.paquetes = []

    def ejecutar(self):
        """
        Método de arranque.
        Inicializa la ventana gráfica y lanza el bucle infinito.
        """
        # 1. Configuración de ventana (Ancho 256, Alto 128)
        pyxel.init(256, 128, title="Mario Bros")

        # 2. Carga de recursos (imágenes y tilemaps)
        pyxel.load("recursos.pyxres")

        # 3. Inicialización del sistema de sonido (ahora que Pyxel existe)
        self.sonido = GestorSonido()

        # 4. Aseguramos que el jefe empiece oculto
        self.jefe.desaparecer()

        # 5. LANZAMIENTO DEL BUCLE PRINCIPAL
        # Pyxel llamará a self.update() y self.draw() 30 veces por segundo
        pyxel.run(self.update, self.draw)

    # =========================================================================
    # SISTEMA DE PERSISTENCIA (GUARDAR DATOS)
    # =========================================================================

    def cargar_record(self) -> int:
        """Intenta leer el archivo 'record.txt' para obtener la puntuación máxima."""
        if os.path.exists("record.txt"):
            try:
                archivo = open("record.txt", "r")
                contenido = archivo.read()
                valor = int(contenido)
                archivo.close()
                return valor
            except:
                return 0 # Si falla la lectura, devolvemos 0
        return 0

    def guardar_record(self):
        """Escribe la puntuación actual en 'record.txt' si es un nuevo récord."""
        if self.puntuacion > self.record_actual:
            self.record_actual = self.puntuacion
            try:
                archivo = open("record.txt", "w")
                archivo.write(str(self.record_actual))
                archivo.close()
            except:
                pass # Ignoramos errores de escritura

    # =========================================================================
    # BUCLE DE LÓGICA (UPDATE)
    # =========================================================================

    def update(self):
        """
        Gestor central de lógica.
        Delega la actualización según en qué pantalla estemos.
        """

        # Máquina de estados de la aplicación
        if self.estado == "menu":
            # En el menú sí permitimos salir con ESCAPE directamente
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()
            self._update_menu()

        elif self.estado == "config":
            # En config, ESCAPE vuelve al menú
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                self.estado = "menu"
            self._update_config()

        elif self.estado == "juego":
            # DETECCIÓN DE PAUSA: Tecla 'P' o 'ESCAPE'
            if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.estado = "pausa"
                self.pausa_cursor = 0        # Reseteamos cursor
                self.sonido.detener_musica() # Feedback auditivo
            else:
                self._update_juego()

        elif self.estado == "pausa":
            self._update_pausa()

    def _update_menu(self):
        """Lógica del Menú Principal."""
        # Control de flechas para mover opción
        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_opcion = (self.menu_opcion - 1) % 2

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_opcion = (self.menu_opcion + 1) % 2

        # Selección (Enter)
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_opcion == 0:
                self.estado = "config" # Ir a configurar partida
            elif self.menu_opcion == 1:
                pyxel.quit()           # Salir

    def _update_config(self):
        """Lógica del Menú de Configuración."""
        # Navegación vertical entre opciones
        if pyxel.btnp(pyxel.KEY_UP):
            self.config_cursor = (self.config_cursor - 1) % 4

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.config_cursor = (self.config_cursor + 1) % 4

        # Modificar valores (Izquierda/Derecha) según dónde esté el cursor
        if self.config_cursor == 0:  # Opción: Velocidad
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.config_vel_index = (self.config_vel_index - 1) % 4
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_vel_index = (self.config_vel_index + 1) % 4

        elif self.config_cursor == 1:  # Opción: Número de Paquetes
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                self.config_paquetes_index = 1 - self.config_paquetes_index

        # Botón Enter para confirmar acciones
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.config_cursor == 2:  # EMPEZAR PARTIDA
                self.iniciar_partida()
            elif self.config_cursor == 3:  # VOLVER AL MENU
                self.sonido.detener_musica()
                self.estado = "menu"

    def _update_pausa(self):
        """Lógica del Menú de Pausa (Flotante)."""
        # Navegación arriba/abajo
        if pyxel.btnp(pyxel.KEY_UP):
            self.pausa_cursor = (self.pausa_cursor - 1) % 2

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.pausa_cursor = (self.pausa_cursor + 1) % 2

        # Selección con ENTER
        if pyxel.btnp(pyxel.KEY_RETURN):

            # Opción 0: CONTINUAR
            if self.pausa_cursor == 0:
                self.estado = "juego"
                self.sonido.reproducir_musica_juego()

            # Opción 1: SALIR AL MENU
            elif self.pausa_cursor == 1:
                self.estado = "menu"
                self.sonido.detener_musica()

        # Tecla rápida para volver al juego (P o ESC)
        if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.estado = "juego"
            self.sonido.reproducir_musica_juego()

    # =========================================================================
    # LÓGICA DE JUEGO (GAMEPLAY)
    # =========================================================================

    def iniciar_partida(self):
        """Resetea todas las variables para comenzar una partida limpia."""
        self.puntuacion = 0
        self.fallos = 0
        self.game_over = False

        # Recargamos el récord por si cambió
        self.record_actual = self.cargar_record()

        # Reseteo del Camión
        self.camion.carga = 0
        self.camion.estado = Camion.PARADO
        self.camion.x = 8
        self.camion.y = 64
        self.camion.reparto_terminado = False

        # Reseteo de Personajes (todos al piso 0)
        self.mario.piso = 0
        self.luigi.piso = 0
        self.mario.y = self.pisos[0]
        self.luigi.y = self.pisos[0]

        # Reseteo del Jefe
        self.jefe.desaparecer()
        self.jefe_timer = 0
        self.shake = 0

        # Configuración de Dificultad (Aplicamos lo elegido en el menú)
        Paquete.VX = self.velocidades[self.config_vel_index]

        if self.config_paquetes_index == 0:
            self.num_paquetes = 1
        else:
            self.num_paquetes = 2

        # Creación de los paquetes
        self._crear_paquetes()

        # Iniciamos música y cambiamos estado
        self.estado = "juego"
        self.sonido.reproducir_musica_juego()

    def _crear_paquetes(self):
        """Instancia los objetos paquete y los añade a la lista."""
        self.paquetes = []

        # Paquete 1: Siempre activo al inicio
        p1 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
        p1.reiniciar_salida()
        self.paquetes.append(p1)

        # Paquete 2: Si está configurado, se crea pero INACTIVO
        if self.num_paquetes == 2:
            p2 = Paquete(Paquete.COL_SALIDA_X * 8, Paquete.PISOS_Y[0] * 8)
            p2.reiniciar_salida()
            p2.activo = False
            self.paquetes.append(p2)

    def _update_juego(self):
        """
        BUCLE PRINCIPAL DEL GAMEPLAY.
        Gestiona prioridades: Game Over > Jefe > Juego Normal.
        """

        # 1. Si hemos perdido, solo esperamos tecla de reinicio
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.iniciar_partida()
            return

        # 2. Si el Jefe está regañando (animación de fallo)
        if self.jefe_timer > 0:
            self.jefe_timer = self.jefe_timer - 1
            self.jefe.update()

            # Nota: Los paquetes que estén cayendo deben seguir cayendo
            # para que se vea cómo se pierden en el vacío.
            for p in self.paquetes:
                if p.estado == "caida_fallo":
                    p.update(self.mario, self.luigi, self)

            # Efecto de terremoto
            self.shake = 3

            # Cuando termina la regañina...
            if self.jefe_timer <= 0:
                self.jefe.desaparecer()
                self.shake = 0

                # Reiniciamos los paquetes válidos para seguir jugando
                for p in self.paquetes:
                    if p.activo == False:
                        p.reiniciar_salida()
                        p.activo = True
            return

        # 3. Lógica Normal del Juego

        self.camion.update()

        # Comprobar si el camión ha vuelto de repartir para sacar nuevos paquetes
        if self.camion.reparto_terminado:
            self.camion.reparto_terminado = False
            self._crear_paquetes()

        # Si el camión está en "DESCANSO", congelamos el juego (return)
        if self.camion.estado == Camion.FUERA:
            return

        # --- Controles de Personajes ---
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.mover_arriba()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.mover_abajo()

        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.mover_arriba()
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.mover_abajo()

        # --- Gestión inteligente del 2º Paquete ---
        if self.num_paquetes == 2:
            if len(self.paquetes) > 1:
                p1 = self.paquetes[0]
                p2 = self.paquetes[1]

                # Regla: El paquete 2 solo sale si el 1 ya ha avanzado lo suficiente
                # (está en el piso 2 y ha pasado la zona de peligro)
                distancia_segura = p1.x <= Paquete.COL_COL_CONTACTO_DER * 8

                if p2.activo == False and p1.piso == 2 and distancia_segura:
                    p2.reiniciar_salida()
                    p2.activo = True

        # --- Actualizar Paquetes ---
        for p in self.paquetes:
            # Pasamos las referencias de mario/luigi y self (Juego)
            p.update(self.mario, self.luigi, self)

        # --- Verificar Game Over ---
        if self.fallos >= 3:
            self.game_over = True
            self.guardar_record()
            self.sonido.sfx_game_over()

    def invocar_jefe(self):
        """Método llamado por un Paquete cuando detecta un error."""
        self.jefe.aparecer()
        self.jefe_timer = 120 # Duración de la regañina (frames)
        self.shake = 3        # Intensidad del temblor
        self.sonido.sfx_fallo()

    # =========================================================================
    # BUCLE DE DIBUJADO (DRAW)
    # =========================================================================
    def draw(self):
        """Distribuidor de dibujado según pantalla."""
        if self.estado == "menu":
            self.hud.draw_menu(self.menu_opcion)

        elif self.estado == "config":
            vt = self.velocidades_texto[self.config_vel_index]
            self.hud.draw_config(self.config_cursor, vt, self.num_paquetes)

        elif self.estado == "juego":
            self._draw_juego()

        elif self.estado == "pausa":
            # TRUCO: Primero dibujamos el juego DE FONDO
            self._draw_juego()
            # Luego dibujamos la ventana de pausa ENCIMA
            self.hud.draw_pausa(self.pausa_cursor, self.puntuacion)

    def _draw_juego(self):
        """Dibuja todos los elementos de la partida."""
        pyxel.cls(7) # Fondo blanco (o color base)

        # Cálculo del temblor (Shake) si el jefe está activo
        dx = 0
        dy = 0
        if self.jefe_timer > 0:
            dx = pyxel.rndi(-self.shake, self.shake)
            dy = pyxel.rndi(-self.shake, self.shake)

        # 1. Fondo (Tilemap) con desplazamiento de temblor
        pyxel.bltm(dx, dy, 0, 0, 0, pyxel.tilemaps[0].width, pyxel.tilemaps[0].height, colkey=7)

        # 2. Entidades (Personajes y Camión)
        self.camion.draw()
        pyxel.blt(self.luigi.x + dx, self.luigi.y + dy, *self.luigi.sprite_luigi)
        pyxel.blt(self.mario.x + dx, self.mario.y + dy, *self.mario.sprite_mario)

        # 3. Paquetes (se dibujan encima de cintas y personajes)
        for p in self.paquetes:
            p.draw()

        # 4. Jefe (si es visible)
        self.jefe.draw()

        # 5. Interfaz (HUD) - Siempre encima de todo
        self.hud.draw_marcador_juego(self.puntuacion, self.record_actual, self.fallos, self.camion.carga)

        # Mensajes superpuestos
        if self.camion.estado == Camion.FUERA:
            self.hud.draw_mensaje_descanso()

        if self.game_over:
            # Comprobamos si es récord para mostrar mensaje especial
            nuevo_record = False
            if self.puntuacion >= self.record_actual and self.puntuacion > 0:
                nuevo_record = True

            self.hud.draw_game_over(self.puntuacion, self.record_actual, nuevo_record)