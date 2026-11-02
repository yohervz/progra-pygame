"""
Escena Principal de Juego (PlayScene).

¡Aquí ocurre toda la magia de tu juego de plataformas!
Esta escena se encarga de:
- Cargar tu nivel desde 'assets/levels/level_1.txt'.
- Conectar a tu personaje con la física y los controles.
- Mover a los enemigos y comprobar colisiones.
- Hacer que la cámara siga a tu personaje suavemente.
- Detectar si ganaste (al llegar a la meta 'G') o si perdiste todas tus vidas.
"""

from pathlib import Path
from typing import Optional
import pygame

import settings
from game.core.scene import Scene
from game.systems.physics import PhysicsSystem
from game.systems.camera import Camera
from game.systems.level_loader import LevelLoader, LevelData
from game.ui.hud import HUD
from game.entities.enemy import Enemy


class PlayScene(Scene):
    """
    Escena interactiva donde juegas tu nivel.
    """

    def __init__(self, manager) -> None:
        super().__init__(manager)

        # Sistemas que hacen funcionar tu mundo
        self.physics = PhysicsSystem()
        self.camera = Camera()
        self.hud = HUD()

        # Ruta de tu mapa
        self.level_path = settings.LEVELS_DIR / "level_1.txt"
        self.level_data: LevelData = LevelData()

        self.score: int = 0
        self.level_name: str = "Nivel 1 - El Comienzo"

        # Fondo de pantalla: Si agregas 'assets/images/background.png', se usará como imagen;
        # si no, se pintará con el color COLOR_BACKGROUND de settings.py
        self.background_image = self._load_background_image()

    def _load_background_image(self) -> Optional[pygame.Surface]:
        bg_path = settings.IMAGES_DIR / "background.png"
        if bg_path.exists():
            try:
                loaded = pygame.image.load(str(bg_path))
                if pygame.display.get_surface() is not None:
                    loaded = loaded.convert()
                return pygame.transform.scale(loaded, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            except pygame.error as err:
                print(f"[Aviso] No se pudo cargar tu fondo '{bg_path}': {err}")
        return None

    def on_enter(self, **kwargs) -> None:
        """Reinicia tu nivel y tus puntos cada vez que comienzas una partida."""
        self._load_current_level()

    def _load_current_level(self) -> None:
        """Lee tu archivo de mapa y prepara a tu personaje, enemigos y plataformas."""
        # Si no tienes level_1.txt, intentamos cargar level_1.json
        if not self.level_path.exists():
            alt_json = settings.LEVELS_DIR / "level_1.json"
            if alt_json.exists():
                self.level_path = alt_json

        self.level_data = LevelLoader.load_level(self.level_path)
        self.camera.set_world_bounds(self.level_data.width, self.level_data.height)
        self.score = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Atajos útiles mientras juegas:
        - [ESC]: Regresas al Menú Principal.
        - [R]: Reinicias el nivel al instante (muy cómodo para probar tus cambios).
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.change_scene("menu")
            elif event.key == pygame.K_r:
                self._load_current_level()

    def update(self, dt: float) -> None:
        player = self.level_data.player
        if player is None:
            return

        # 1. Leemos las teclas que estás presionando
        player.handle_input()

        # 2. Aplicamos la física: gravedad, suelo, paredes y salto sobre enemigos
        self.physics.update_player(
            player=player,
            platforms=self.level_data.platforms,
            enemies=self.level_data.enemies,
            dt=dt,
            on_enemy_stomped=self._on_enemy_stomped
        )

        # 3. Actualizamos a tu personaje y a los enemigos
        player.update(dt)
        for enemy in self.level_data.enemies:
            enemy.update(dt)

        # 4. Movemos la cámara para que siga a tu personaje
        self.camera.update(player)

        # 5. Si te caes al abismo por debajo del mapa, pierdes todas tus vidas
        if player.y > self.level_data.height + 100:
            player.take_damage(player.max_health)

        # 6. ¿Perdiste todas tus vidas? Viajamos a la pantalla de Game Over
        if not player.is_alive():
            self.manager.change_scene("game_over", victory=False, score=self.score)
            return

        # 7. ¿Tocaste la bandera de meta? ¡Ganaste el nivel!
        if self.level_data.goal_rect and player.rect.colliderect(self.level_data.goal_rect):
            self.score += 500  # Bonificación de 500 puntos por ganar
            self.manager.change_scene("game_over", victory=True, score=self.score)

    def _on_enemy_stomped(self, enemy: Enemy) -> None:
        """Se ejecuta cuando pisas la cabeza de un enemigo: ¡te sumamos 100 puntos!"""
        self.score += 100

    def render(self, surface: pygame.Surface) -> None:
        # 1. Fondo de tu mundo (imagen personalizada o color de settings.py)
        if self.background_image is not None:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(settings.COLOR_BACKGROUND)

        # 2. Dibujamos tus plataformas desplazadas por la cámara
        for plat in self.level_data.platforms:
            screen_rect = self.camera.apply(plat)
            # Solo dibujamos lo que cabe en pantalla para no gastar recursos innecesarios
            if surface.get_rect().colliderect(screen_rect):
                surface.blit(plat.image, screen_rect)

        # 3. Dibujamos la bandera de Meta ('G')
        if self.level_data.goal_rect:
            goal_screen_rect = self.camera.apply(self.level_data.goal_rect)
            if surface.get_rect().colliderect(goal_screen_rect):
                self._draw_goal(surface, goal_screen_rect)

        # 4. Dibujamos a los enemigos activos
        for enemy in self.level_data.enemies:
            if enemy.is_alive:
                screen_rect = self.camera.apply(enemy)
                if surface.get_rect().colliderect(screen_rect):
                    surface.blit(enemy.image, screen_rect)

        # 5. Dibujamos a tu personaje
        if self.level_data.player:
            player_rect = self.camera.apply(self.level_data.player)
            surface.blit(self.level_data.player.image, player_rect)

        # 6. Dibujamos el HUD (vidas y puntos fijos en tu pantalla)
        if self.level_data.player:
            self.hud.render(surface, self.level_data.player, self.score, self.level_name)

    def _draw_goal(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Dibuja una bandera dorada en el bloque de meta."""
        # Mástil
        pygame.draw.rect(surface, (180, 180, 180), (rect.x + 6, rect.y, 4, rect.height))
        # Bandera triangular
        flag_points = [
            (rect.x + 10, rect.y),
            (rect.x + rect.width, rect.y + rect.height // 3),
            (rect.x + 10, rect.y + 2 * (rect.height // 3))
        ]
        pygame.draw.polygon(surface, settings.COLOR_FALLBACK_COIN, flag_points)
