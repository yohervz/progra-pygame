"""
Interfaz en Pantalla (HUD - Heads-Up Display).

El HUD es la capa visual que siempre permanece fija en tu pantalla, sin importar
hacia dónde se mueva la cámara. Aquí se muestra:
- Tus vidas o salud restante.
- Tu puntaje acumulado.
- El nombre del nivel actual.
- Un recordatorio de los controles del juego.
"""

import pygame

import settings
from game.entities.player import Player


class HUD:
    """
    Dibuja tu información de juego (vidas, puntaje y ayudas) fija en la pantalla.
    """

    def __init__(self) -> None:
        # Cargamos las fuentes para escribir textos en pantalla
        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("arial", 14)

    def render(
        self,
        surface: pygame.Surface,
        player: Player,
        score: int = 0,
        level_name: str = "Nivel 1"
    ) -> None:
        """
        Dibuja los indicadores del juego en tu pantalla.
        """
        # 1. Indicador visual de tus vidas
        self._draw_health_bar(surface, player.health, player.max_health)

        # 2. Tu puntaje actual
        score_text = self.font.render(f"PUNTAJE: {score:04d}", True, settings.COLOR_TEXT)
        surface.blit(score_text, (surface.get_width() - 170, 15))

        # 3. Nombre del nivel que estás jugando
        level_text = self.small_font.render(level_name, True, (180, 190, 205))
        surface.blit(level_text, (surface.get_width() - 170, 42))

        # 4. Recordatorio de los controles en la parte inferior
        controls_hint = self.small_font.render(
            "[A/D / Flechas] Moverse  |  [Espacio] Saltar  |  [ESC] Menú",
            True,
            (150, 155, 170)
        )
        surface.blit(controls_hint, (20, surface.get_height() - 25))

    def _draw_health_bar(self, surface: pygame.Surface, current_hp: int, max_hp: int) -> None:
        """
        Dibuja los cuadros o corazones de tu salud:
        - Rojos si están activos.
        - Grises oscuros si has perdido esa vida.
        """
        start_x = 20
        start_y = 18
        heart_size = 20
        gap = 8

        label = self.font.render("VIDAS:", True, settings.COLOR_TEXT)
        surface.blit(label, (start_x, start_y))
        x_offset = start_x + label.get_width() + 10

        for i in range(max_hp):
            box_rect = pygame.Rect(x_offset + i * (heart_size + gap), start_y + 2, heart_size, heart_size)
            if i < current_hp:
                # Vida disponible (color rojo activo)
                pygame.draw.rect(surface, settings.COLOR_HEALTH, box_rect, border_radius=4)
            else:
                # Vida perdida (silueta oscura)
                pygame.draw.rect(surface, (60, 65, 75), box_rect, border_radius=4)
            # Borde exterior
            pygame.draw.rect(surface, (200, 200, 200), box_rect, width=2, border_radius=4)
