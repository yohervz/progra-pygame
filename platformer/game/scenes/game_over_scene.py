"""
Escena de Fin de Partida (GameOverScene).

Esta pantalla se muestra al finalizar tu partida:
- Si lograste llegar a la meta: ¡Muestra felicitaciones de victoria!
- Si perdiste todas tus vidas: Te da la opción de volver a intentarlo.
- Muestra el puntaje final que conseguiste.
"""

import sys
import pygame

import settings
from game.core.scene import Scene


class GameOverScene(Scene):
    """
    Pantalla de resultado (Victoria o Derrota) tras jugar un nivel.
    """

    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 16)

        self.victory: bool = False
        self.score: int = 0

    def on_enter(self, victory: bool = False, score: int = 0, **kwargs) -> None:
        """Recibe el resultado de tu partida desde PlayScene."""
        self.victory = victory
        self.score = score

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Tus opciones al terminar la partida:
        - [ESPACIO] o [R]: Vuelves a jugar de inmediato.
        - [M]: Regresas al Menú Principal.
        - [ESC] o [Q]: Cierras el juego.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_r:
                self.manager.change_scene("play")
            elif event.key == pygame.K_m:
                self.manager.change_scene("menu")
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BACKGROUND)
        center_x = surface.get_width() // 2

        # 1. Título de Victoria o Derrota según tu resultado
        if self.victory:
            title_text = "¡FELICITACIONES! ¡NIVEL COMPLETADO!"
            title_color = (46, 204, 113)  # Verde victoria
        else:
            title_text = "GAME OVER"
            title_color = (231, 76, 60)   # Rojo derrota

        title_surf = self.title_font.render(title_text, True, title_color)
        surface.blit(title_surf, title_surf.get_rect(center=(center_x, 180)))

        # 2. Puntaje que alcanzaste
        score_surf = self.text_font.render(f"Puntaje Final: {self.score}", True, settings.COLOR_TEXT)
        surface.blit(score_surf, score_surf.get_rect(center=(center_x, 260)))

        # 3. Opciones de navegación
        restart_surf = self.text_font.render("[ ESPACIO / R ] Jugar de nuevo", True, settings.COLOR_WHITE)
        surface.blit(restart_surf, restart_surf.get_rect(center=(center_x, 350)))

        menu_surf = self.text_font.render("[ M ] Volver al Menú Principal", True, (180, 190, 205))
        surface.blit(menu_surf, menu_surf.get_rect(center=(center_x, 400)))

        quit_surf = self.small_font.render("[ ESC / Q ] Salir", True, (130, 135, 145))
        surface.blit(quit_surf, quit_surf.get_rect(center=(center_x, 460)))
