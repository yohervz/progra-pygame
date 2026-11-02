"""
Entidad Enemy: Los Enemigos de tu Juego.

Este enemigo patrulla de izquierda a derecha.
- Si tu personaje choca contra él por el costado, ¡te quitará una vida!
- Si saltas y caes sobre su cabeza, ¡lo derrotarás al estilo clásico de plataformas!
- También incluye un dibujo de respaldo con púas y ojos enojados si aún no colocas
  tu propio 'assets/images/enemy.png'.

¡RETO PARA TI!:
¿Te animas a crear un enemigo volador, uno que dispare proyectiles o un jefe final?
"""

from pathlib import Path
from typing import Optional
import pygame

import settings


class Enemy(pygame.sprite.Sprite):
    """
    Enemigo patrullero que vigila una zona de tu nivel.
    """

    def __init__(
        self,
        x: float,
        y: float,
        patrol_distance: int = 120,
        width: int = 32,
        height: int = 32,
        image_path: Optional[Path] = None
    ) -> None:
        super().__init__()

        self.width = width
        self.height = height

        self.start_x = float(x)
        self.x = float(x)
        self.y = float(y)

        # Distancia máxima que recorrerá antes de dar la vuelta
        self.patrol_distance = patrol_distance
        self.min_x = self.start_x - patrol_distance
        self.max_x = self.start_x + patrol_distance

        self.speed = settings.ENEMY_SPEED
        self.vx = self.speed
        self.vy = 0.0

        self.is_alive = True
        self.image_path = image_path if image_path else (settings.IMAGES_DIR / "enemy.png")

        # Cargar tu sprite o generar el dibujo de respaldo con púas
        self.base_image = self._load_image_or_fallback(self.image_path)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=(int(self.x), int(self.y)))

    def _load_image_or_fallback(self, image_path: Path) -> pygame.Surface:
        """
        Carga la imagen del enemigo si la colocas en 'assets/images/enemy.png'.
        Si aún no la tienes, dibuja un enemigo rojo con ojos y púas.
        """
        if image_path.exists():
            try:
                loaded = pygame.image.load(str(image_path))
                if pygame.display.get_surface() is not None:
                    loaded = loaded.convert_alpha()
                return pygame.transform.scale(loaded, (self.width, self.height))
            except pygame.error as err:
                print(f"[Aviso] No se pudo cargar tu sprite enemigo '{image_path}': {err}")

        # --- DIBUJO DE RESPALDO PARA EL ENEMIGO ---
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 4, self.width, self.height - 4)

        # 1. Cuerpo
        pygame.draw.rect(surface, settings.COLOR_FALLBACK_ENEMY, rect, border_radius=4)

        # 2. Púas triangulares
        points_spike = [
            (self.width // 4, 4),
            (self.width // 2, 0),
            (3 * self.width // 4, 4)
        ]
        pygame.draw.polygon(surface, settings.COLOR_FALLBACK_ENEMY, points_spike)

        # 3. Ojos enojados
        eye_y = 14
        pygame.draw.circle(surface, settings.COLOR_WHITE, (10, eye_y), 4)
        pygame.draw.circle(surface, settings.COLOR_WHITE, (self.width - 10, eye_y), 4)
        pygame.draw.circle(surface, settings.COLOR_BLACK, (11, eye_y), 2)
        pygame.draw.circle(surface, settings.COLOR_BLACK, (self.width - 9, eye_y), 2)

        return surface

    def update(self, dt: float) -> None:
        """
        Mueve al enemigo de un lado a otro e invierte su dirección al llegar a los límites.
        """
        if not self.is_alive:
            return

        self.x += self.vx * dt
        self.rect.x = int(self.x)

        # Si llega al extremo derecho, gira a la izquierda
        if self.x >= self.max_x:
            self.vx = -abs(self.speed)
            self.image = pygame.transform.flip(self.base_image, True, False)
        # Si llega al extremo izquierdo, gira a la derecha
        elif self.x <= self.min_x:
            self.vx = abs(self.speed)
            self.image = self.base_image.copy()

    def reverse_direction(self) -> None:
        """Invierte la marcha del enemigo si choca con una pared o un obstáculo."""
        self.vx = -self.vx
        if self.vx < 0:
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.image = self.base_image.copy()

    def defeat(self) -> None:
        """
        Se ejecuta cuando saltas sobre la cabeza del enemigo:
        lo elimina del juego para que no siga molestándote.
        """
        self.is_alive = False
        self.kill()
