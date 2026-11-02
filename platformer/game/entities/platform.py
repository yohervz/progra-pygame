"""
Entidad Platform: Los Bloques y Plataformas de tu Mundo.

Representa los bloques sólidos donde tu personaje y los enemigos pueden caminar.
- Si colocas una imagen en 'assets/images/platform.png', todas tus plataformas
  se vestirán automáticamente con esa textura.
- Si no tienes imagen todavía, dibujará un bloque verde con césped superior como respaldo.

¡RETO PARA TI!:
¿Quieres plataformas que se muevan solas, que desaparezcan al pisarlas o que reboten?
¡Puedes programarlo en el método `update()` de esta clase!
"""

from pathlib import Path
from typing import Optional
import pygame

import settings


class Platform(pygame.sprite.Sprite):
    """
    Bloque sólido del escenario sobre el cual puedes pararte.
    """

    # Memoria caché para que tu juego sea súper veloz y no reescale la misma imagen 100 veces
    _cached_surfaces = {}

    def __init__(
        self,
        x: float,
        y: float,
        width: int = settings.TILE_SIZE,
        height: int = settings.TILE_SIZE,
        image_path: Optional[Path] = None,
        color: tuple = settings.COLOR_FALLBACK_PLATFORM
    ) -> None:
        super().__init__()
        self.width = width
        self.height = height

        # Si no le indicas una imagen distinta, usará 'assets/images/platform.png'
        self.image_path = Path(image_path) if image_path else (settings.IMAGES_DIR / "platform.png")
        self.image = self._load_image_or_fallback(self.image_path, color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def _load_image_or_fallback(self, image_path: Optional[Path], color: tuple) -> pygame.Surface:
        """
        Carga tu textura desde el disco. Si aún no tienes archivo de imagen,
        dibuja automáticamente un bloque con borde y franja superior de césped.
        """
        cache_key = (str(image_path), self.width, self.height)
        if cache_key in Platform._cached_surfaces:
            return Platform._cached_surfaces[cache_key]

        if image_path is not None and Path(image_path).exists():
            try:
                loaded = pygame.image.load(str(image_path))
                if pygame.display.get_surface() is not None:
                    loaded = loaded.convert_alpha()
                surface = pygame.transform.scale(loaded, (self.width, self.height))
                Platform._cached_surfaces[cache_key] = surface
                return surface
            except pygame.error as err:
                print(f"[Aviso] No se pudo cargar tu imagen de plataforma '{image_path}': {err}")

        # --- DIBUJO DE RESPALDO (Por si aún no tienes textura) ---
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Relleno del bloque
        surface.fill(color)
        # Borde exterior
        darker = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
        pygame.draw.rect(surface, darker, surface.get_rect(), width=2)
        # Franja superior que simula césped
        top_accent = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
        pygame.draw.rect(surface, top_accent, (0, 0, self.width, max(4, self.height // 6)))

        Platform._cached_surfaces[cache_key] = surface
        return surface

    def update(self, dt: float) -> None:
        """
        Las plataformas iniciales son estáticas.
        
        ¡TU TURNO!:
        Si quieres crear plataformas móviles, puedes darles una velocidad
        (por ejemplo `self.vx = 2.0`) y sumar `self.rect.x += self.vx * dt` aquí.
        """
        pass
