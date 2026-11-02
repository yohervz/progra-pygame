"""
Clase Game: El motor y bucle principal de tu juego.

Aquí se crea la ventana de tu juego, se enciende Pygame, se sincroniza el reloj
a los fotogramas configurados en settings.py y se repite el bucle infinito:
1. Escuchar eventos (teclado, mouse, cerrar ventana).
2. Actualizar la lógica del juego.
3. Dibujar todo en la pantalla.
4. Refrescar la imagen para el jugador.
"""

import sys
import pygame

import settings
from game.core.scene_manager import SceneManager
from game.scenes.menu_scene import MenuScene
from game.scenes.play_scene import PlayScene
from game.scenes.game_over_scene import GameOverScene


class Game:
    """
    Controlador maestro de tu juego.
    
    Gestiona la ventana y ejecuta el bucle principal mientras juegas.
    """

    def __init__(self) -> None:
        pygame.init()
        # Inicializamos el soporte para textos y fuentes
        pygame.font.init()
        # Inicializamos el sonido de forma segura (si tu computadora no tiene parlantes, no fallará)
        try:
            pygame.mixer.init()
        except pygame.error:
            print("[Aviso] No se detectó dispositivo de audio. Tu juego continuará funcionando sin sonido.")

        # Creamos tu ventana con las medidas que definiste en settings.py
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        # Creamos el gestor que cambiará tus pantallas
        self.scene_manager = SceneManager()
        self._init_scenes()

    def _init_scenes(self) -> None:
        """
        Aquí registras todas las pantallas que tenga tu juego.
        ¡Si creas una pantalla nueva (ej. créditos o tienda), regístrala aquí!
        """
        self.scene_manager.register_scene("menu", MenuScene(self.scene_manager))
        self.scene_manager.register_scene("play", PlayScene(self.scene_manager))
        self.scene_manager.register_scene("game_over", GameOverScene(self.scene_manager))

        # Le decimos al juego que inicie en el Menú Principal
        self.scene_manager.change_scene("menu")

    def run(self) -> None:
        """
        Bucle Principal (Game Loop).
        Este 'while' se repite 60 veces por segundo mientras estés jugando.
        """
        while self.running:
            # Calculamos 'dt' (delta time):
            # A 60 FPS ideales, dt vale aproximadamente 1.0. Si la computadora se ralentiza,
            # dt sube un poco para compensar y que tu personaje no se mueva en cámara lenta.
            dt_raw = self.clock.tick(settings.FPS) / 1000.0
            dt = min(dt_raw * 60.0, 3.0)  # Límite de seguridad para evitar saltos bruscos

            # 1. Eventos: Comprobamos si el usuario presionó la 'X' de la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    # Le pasamos las teclas a la escena activa
                    self.scene_manager.handle_event(event)

            # 2. Lógica: Movemos personajes, aplicamos física y colisiones
            self.scene_manager.update(dt)

            # 3. Dibujo: Limpiamos la pantalla con el color de fondo y dibujamos la escena
            self.screen.fill(settings.COLOR_BACKGROUND)
            self.scene_manager.render(self.screen)

            # 4. Refresco: Mostramos el nuevo fotograma en tu monitor
            pygame.display.flip()

        self.quit()

    def quit(self) -> None:
        """Cierra tu juego y libera la memoria limpiamente."""
        pygame.quit()
        sys.exit()
