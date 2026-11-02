"""
Sistema de Cámara (Camera 2D).

¿Por qué necesitas una cámara?
En un juego de plataformas, tu nivel puede ser mucho más ancho y alto que tu pantalla.
La cámara se encarga de:
1. Seguir a tu personaje suavemente hacia donde vaya.
2. Transformar las posiciones del mundo a las coordenadas visibles de tu ventana.
3. Detenerse al llegar a los bordes del mapa para que nunca se vea un vacío negro fuera del escenario.
"""

from typing import Union
import pygame

import settings


class Camera:
    """
    Cámara 2D que persigue a tu personaje con movimiento suave.
    """

    def __init__(
        self,
        viewport_width: int = settings.SCREEN_WIDTH,
        viewport_height: int = settings.SCREEN_HEIGHT,
        smooth_factor: float = 0.1
    ) -> None:
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        # Qué tan rápido reacciona la cámara: 0.1 es suave, 1.0 es instantáneo y rígido
        self.smooth_factor = smooth_factor

        self.x = 0.0
        self.y = 0.0

        # Dimensiones totales de tu mapa
        self.world_width = viewport_width
        self.world_height = viewport_height

    def set_world_bounds(self, width: int, height: int) -> None:
        """
        Configura los límites totales de tu nivel para que la cámara no se salga del mapa.
        """
        self.world_width = max(width, self.viewport_width)
        self.world_height = max(height, self.viewport_height)

    def update(self, target: pygame.sprite.Sprite) -> None:
        """
        Mueve la cámara suavemente (con interpolación lineal / lerp) para mantener
        a tu personaje centrado en la pantalla.
        """
        # Calculamos la posición donde tu personaje queda centrado
        target_x = target.rect.centerx - self.viewport_width / 2.0
        target_y = target.rect.centery - self.viewport_height / 2.0

        # Suavizado de desplazamiento
        self.x += (target_x - self.x) * self.smooth_factor
        self.y += (target_y - self.y) * self.smooth_factor

        # Evitamos que la cámara muestre espacio fuera de los bordes de tu nivel
        max_x = self.world_width - self.viewport_width
        max_y = self.world_height - self.viewport_height

        self.x = max(0.0, min(self.x, max_x))
        self.y = max(0.0, min(self.y, max_y))

    def apply(self, entity_or_rect: Union[pygame.sprite.Sprite, pygame.Rect]) -> pygame.Rect:
        """
        Convierte la posición real de un objeto en el mundo a la posición
        donde debe dibujarse en tu pantalla.
        """
        if isinstance(entity_or_rect, pygame.Rect):
            rect = entity_or_rect
        else:
            rect = entity_or_rect.rect

        return rect.move(int(-self.x), int(-self.y))
