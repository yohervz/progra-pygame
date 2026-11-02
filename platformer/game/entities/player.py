"""
Entidad Player: Tu Personaje Principal.

Aquí controlas todo lo que puede hacer tu héroe:
- Leer las teclas que presionas para caminar y saltar.
- Gestionar tus vidas y el tiempo de invulnerabilidad tras recibir un golpe.
- Cargar tu imagen personalizada ('assets/images/player.png') o generar un
  personaje de respaldo automático si aún no tienes una imagen lista.

¡RETO PARA TI!:
Revisa los métodos `jump()` y `handle_input()` para agregar mecánicas como
doble salto, agacharse, un impulso tipo dash o efectos de sonido.
"""

from pathlib import Path
from typing import Optional
import pygame

import settings


class Player(pygame.sprite.Sprite):
    """
    Tu personaje jugable dentro del mundo de plataformas.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: int = 32,
        height: int = 48,
        image_path: Optional[Path] = None
    ) -> None:
        super().__init__()

        self.width = width
        self.height = height

        # Posición en punto flotante para que tu movimiento sea suave y preciso
        self.x = float(x)
        self.y = float(y)

        # Velocidades actuales en X (horizontal) e Y (vertical)
        self.vx = 0.0
        self.vy = 0.0

        # Estados de física: ¿estás tocando el suelo? ¿hacia dónde estás mirando?
        self.is_grounded = False
        self.facing_right = True

        # Tus vidas y sistema de invulnerabilidad temporal al recibir daño
        self.max_health = settings.PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.is_invulnerable = False
        self.invulnerable_timer = 0.0
        self.invulnerable_duration = 1.5  # Segundos que parpadeas invulnerable

        # Buscamos tu sprite personalizado en assets/images/player.png
        self.image_path = image_path if image_path else (settings.IMAGES_DIR / "player.png")

        # Cargamos tu imagen, o dibujamos un personaje geométrico si aún no tienes archivo
        self.base_image = self._load_image_or_fallback(self.image_path)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=(int(self.x), int(self.y)))

    def _load_image_or_fallback(self, image_path: Path) -> pygame.Surface:
        """
        Intenta cargar tu imagen. Si todavía no la has colocado en assets/images/,
        ¡no te preocupes! Este método dibuja automáticamente un personaje con ojos
        para que puedas programar y jugar de inmediato.
        """
        if image_path.exists():
            try:
                loaded = pygame.image.load(str(image_path))
                if pygame.display.get_surface() is not None:
                    loaded = loaded.convert_alpha()
                return pygame.transform.scale(loaded, (self.width, self.height))
            except pygame.error as err:
                print(f"[Aviso] No se pudo cargar tu sprite '{image_path}': {err}")

        # --- DIBUJO DE RESPALDO (Por si aún no tienes imagen) ---
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 1. Cuerpo principal
        body_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(surface, settings.COLOR_FALLBACK_PLAYER, body_rect, border_radius=8)

        # 2. Borde sutil
        darker = (30, 100, 160)
        pygame.draw.rect(surface, darker, body_rect, width=2, border_radius=8)

        # 3. Ojos mirando hacia adelante
        pygame.draw.circle(surface, settings.COLOR_WHITE, (self.width - 10, 14), 5)
        pygame.draw.circle(surface, settings.COLOR_BLACK, (self.width - 8, 14), 2)

        return surface

    def handle_input(self) -> None:
        """
        Lee tu teclado en cada fotograma y ajusta tu velocidad.
        Puedes moverte con las flechas o con las teclas A / D.
        """
        keys = pygame.key.get_pressed()

        # Movimiento hacia los lados
        self.vx = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -settings.PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = settings.PLAYER_SPEED
            self.facing_right = True

        # Salto (Espacio, W o Flecha Arriba)
        # Solo te permite saltar si tienes los pies firmes sobre una plataforma
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_grounded:
            self.jump()

    def jump(self) -> None:
        """
        Aplica el impulso hacia arriba para saltar.
        
        ¡TU TURNO!:
        - ¿Quieres un sonido de salto? Carga 'jump.wav' y reprodúcelo aquí con pygame.mixer.Sound.
        - ¿Quieres doble salto? Crea una variable `self.extra_jumps` y descuéntala cada vez que saltes en el aire.
        """
        self.vy = settings.PLAYER_JUMP_FORCE
        self.is_grounded = False

    def take_damage(self, amount: int = 1) -> None:
        """
        Te resta vidas cuando tocas a un enemigo y activa un momento de invulnerabilidad.
        """
        if not self.is_invulnerable and self.health > 0:
            self.health -= amount
            self.is_invulnerable = True
            self.invulnerable_timer = self.invulnerable_duration
            # Pequeño rebote para avisarte que recibiste un golpe
            self.vy = -6.0

    def update(self, dt: float) -> None:
        """
        Actualiza el tiempo de invulnerabilidad y la dirección hacia donde miras.
        (El movimiento y las colisiones con el mapa las resuelve PhysicsSystem).
        """
        # Descontamos el tiempo de invulnerabilidad
        if self.is_invulnerable:
            self.invulnerable_timer -= (dt / 60.0)
            if self.invulnerable_timer <= 0:
                self.is_invulnerable = False

        # Invertimos tu sprite si estás mirando a la izquierda
        if not self.facing_right:
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.image = self.base_image.copy()

        # Efecto de parpadeo visual mientras seas invulnerable
        if self.is_invulnerable:
            alpha = 100 if int(self.invulnerable_timer * 10) % 2 == 0 else 255
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def is_alive(self) -> bool:
        """Te indica si a tu personaje aún le quedan vidas."""
        return self.health > 0

    def reset(self, start_x: float, start_y: float) -> None:
        """Restaura tu posición y vidas para reiniciar la partida."""
        self.x = start_x
        self.y = start_y
        self.vx = 0.0
        self.vy = 0.0
        self.health = self.max_health
        self.is_invulnerable = False
        self.is_grounded = False
        self.rect.topleft = (int(self.x), int(self.y))
