"""
Sistema de Física y Colisiones (PhysicsSystem).

¿Cómo funciona la física en un juego 2D?
1. Aplicamos gravedad jalando hacia abajo la velocidad vertical (`player.vy`).
2. Movemos al personaje horizontalmente y corregimos si choca con una pared.
3. Movemos al personaje verticalmente y corregimos si aterriza en una plataforma o si choca la cabeza contra el techo.
4. Separar las colisiones en el eje X y en el eje Y es el gran secreto de los juegos de plataformas:
   ¡evita que tu personaje quede atrapado dentro de las esquinas o atraviese el suelo!
"""

from typing import List, Callable, Optional
import pygame

import settings
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.platform import Platform


class PhysicsSystem:
    """
    Controla el movimiento, la gravedad y los choques entre tu personaje y el mundo.
    """

    def __init__(self, gravity: float = settings.GRAVITY, max_fall_speed: float = settings.MAX_FALL_SPEED) -> None:
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed

    def update_player(
        self,
        player: Player,
        platforms: List[Platform],
        enemies: List[Enemy],
        dt: float,
        on_enemy_stomped: Optional[Callable[[Enemy], None]] = None
    ) -> None:
        """
        Calcula la física completa de tu personaje en cada fotograma.
        """
        # 1. Aplicamos la gravedad hacia abajo
        player.vy += self.gravity * dt
        if player.vy > self.max_fall_speed:
            player.vy = self.max_fall_speed

        # 2. Paso Horizontal: Mover en X y comprobar paredes
        player.x += player.vx * dt
        player.rect.x = round(player.x)
        self._resolve_horizontal_collisions(player, platforms)

        # 3. Paso Vertical: Mover en Y y comprobar pisos/techos
        player.is_grounded = False  # Asumimos que estás en el aire hasta confirmar contacto con una plataforma
        player.y += player.vy * dt
        player.rect.y = round(player.y)
        self._resolve_vertical_collisions(player, platforms)

        # 4. Comprobamos la interacción con enemigos: ¿lo aplastaste o te hizo daño?
        self._handle_enemy_collisions(player, enemies, on_enemy_stomped)

    def _resolve_horizontal_collisions(self, player: Player, platforms: List[Platform]) -> None:
        """Evita que tu personaje atraviese paredes hacia los lados."""
        for plat in platforms:
            if player.rect.colliderect(plat.rect):
                if player.vx > 0:  # Ibas hacia la derecha y chocaste con el lado izquierdo de un bloque
                    player.rect.right = plat.rect.left
                elif player.vx < 0:  # Ibas hacia la izquierda y chocaste con el lado derecho
                    player.rect.left = plat.rect.right
                # Sincronizamos la posición continua
                player.x = float(player.rect.x)

    def _resolve_vertical_collisions(self, player: Player, platforms: List[Platform]) -> None:
        """Detecta cuándo caes sobre una plataforma para pararte o si te golpeas la cabeza con el techo."""
        for plat in platforms:
            if player.rect.colliderect(plat.rect):
                if player.vy > 0:  # Estabas cayendo: aterrizaste con éxito sobre el suelo
                    player.rect.bottom = plat.rect.top
                    player.vy = 0.0
                    player.is_grounded = True
                elif player.vy < 0:  # Estabas saltando y chocaste tu cabeza contra un bloque superior
                    player.rect.top = plat.rect.bottom
                    player.vy = 0.0
                # Sincronizamos la posición continua
                player.y = float(player.rect.y)

    def _handle_enemy_collisions(
        self,
        player: Player,
        enemies: List[Enemy],
        on_enemy_stomped: Optional[Callable[[Enemy], None]]
    ) -> None:
        """
        Evalúa el contacto con los enemigos activos:
        - Si vienes cayendo desde arriba, pisas al enemigo, lo derrotas y das un salto de rebote.
        - Si lo tocas por el costado o de frente, tu personaje recibe daño y pierde 1 vida.
        """
        for enemy in enemies:
            if not enemy.is_alive:
                continue

            if player.rect.colliderect(enemy.rect):
                # ¿Está tu personaje cayendo y ubicado por encima del centro del enemigo?
                is_falling = player.vy > 0
                is_above = player.rect.centery < enemy.rect.centery

                if is_falling and is_above:
                    # ¡Aplastaste al enemigo!
                    enemy.defeat()
                    player.vy = settings.PLAYER_JUMP_FORCE * 0.65  # Rebote satisfactorio
                    if on_enemy_stomped:
                        on_enemy_stomped(enemy)
                else:
                    # El enemigo te golpeó a ti
                    player.take_damage(1)
