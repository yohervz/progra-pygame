"""
Escena de Menú Principal (MenuScene).

¡Esta es la pantalla de bienvenida de tu juego!
Aquí puedes colocar tu título, instrucciones, opciones y una vista previa
de tus personajes.

¡TU TURNO!:
Puedes agregar música para el menú, botones para seleccionar personajes o
un selector de niveles.
"""

import sys
import pygame

import settings
from game.core.scene import Scene


class MenuScene(Scene):
    """
    Pantalla inicial que te recibe al abrir el juego.
    """

    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.menu_font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 16)
        self.blink_timer = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Escucha tus teclas en el menú:
        - [ESPACIO] o [ENTER]: Inicia tu partida.
        - [Q] o [ESC]: Sale del juego.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                # Cambiamos a la escena donde juegas
                self.manager.change_scene("play")
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def update(self, dt: float) -> None:
        """Controla el efecto de parpadeo del texto para llamar la atención del jugador."""
        self.blink_timer += dt / 60.0

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BACKGROUND)

        # 1. Título principal de tu juego
        title_surf = self.title_font.render("Plantilla para crear juegos", True, settings.COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(surface.get_width() // 2, 160))
        surface.blit(title_surf, title_rect)

        # 2. Decoración: Tu personaje y una plataforma en el centro
        center_x = surface.get_width() // 2
        from game.entities.platform import Platform
        from game.entities.player import Player

        preview_plat = Platform(center_x - 60, 310, width=120, height=20)
        surface.blit(preview_plat.image, preview_plat.rect)

        preview_player = Player(center_x - 16, 260)
        surface.blit(preview_player.image, preview_player.rect)

        # 3. Texto parpadeante que te invita a jugar
        if int(self.blink_timer * 2) % 2 == 0:
            start_surf = self.menu_font.render("Presiona [ ESPACIO ] para jugar", True, settings.COLOR_WHITE)
            start_rect = start_surf.get_rect(center=(surface.get_width() // 2, 400))
            surface.blit(start_surf, start_rect)

        # 4. Opción para salir
        quit_surf = self.small_font.render("Presiona [ Q ] para Salir", True, (160, 165, 175))
        quit_rect = quit_surf.get_rect(center=(surface.get_width() // 2, 450))
        surface.blit(quit_surf, quit_rect)
