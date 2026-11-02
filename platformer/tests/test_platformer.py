"""
Pruebas Unitarias para el Juego de Plataformas.

Verifica:
1. Resistencia ante la falta de sprites (Fallback visual automático).
2. Correctitud del cargador de niveles (LevelLoader).
3. Mecánicas y matemáticas del sistema de física (PhysicsSystem).
4. Gestión de escenas (SceneManager).

Estas pruebas se pueden ejecutar sin abrir una ventana de visualización (modo headless).
"""

import os
import sys
import unittest
from pathlib import Path

# Configurar SDL en modo dummy para poder correr pruebas sin pantalla física
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Asegurar que la ruta 'platformer' esté en sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pygame
pygame.init()
pygame.font.init()

import settings
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.platform import Platform
from game.systems.physics import PhysicsSystem
from game.systems.camera import Camera
from game.systems.level_loader import LevelLoader
from game.core.scene_manager import SceneManager
from game.core.scene import Scene


class DummyScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.entered = False
        self.exited = False
        self.received_data = {}

    def on_enter(self, **kwargs):
        self.entered = True
        self.received_data = kwargs

    def on_exit(self):
        self.exited = True

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass


class TestPlatformer(unittest.TestCase):

    def test_fallback_sprites_without_files(self):
        """
        Comprueba que si aún no tienes imágenes en assets/images/,
        tu juego genera automáticamente figuras de respaldo sin arrojar errores.
        """
        fake_path = Path("/ruta/inexistente/sprite_fantasma.png")

        # Jugador
        player = Player(x=50, y=50, image_path=fake_path)
        self.assertIsNotNone(player.image)
        self.assertEqual(player.image.get_width(), player.width)
        self.assertEqual(player.image.get_height(), player.height)
        self.assertEqual(player.rect.topleft, (50, 50))

        # Enemigo
        enemy = Enemy(x=100, y=100, image_path=fake_path)
        self.assertIsNotNone(enemy.image)
        self.assertEqual(enemy.image.get_width(), enemy.width)
        self.assertEqual(enemy.rect.topleft, (100, 100))

        # Plataforma
        platform = Platform(x=0, y=0, width=40, height=40, image_path=fake_path)
        self.assertIsNotNone(platform.image)
        self.assertEqual(platform.rect.width, 40)
        self.assertEqual(platform.rect.height, 40)

    def test_level_loader_txt_and_json(self):
        """Verifica que el cargador de niveles interprete mapas tanto .txt como .json."""
        level_txt_path = settings.LEVELS_DIR / "level_1.txt"
        self.assertTrue(level_txt_path.exists(), "Debe existir level_1.txt")
        level_data = LevelLoader.load_level(level_txt_path)

        self.assertIsNotNone(level_data.player, "El nivel debe instanciar un jugador")
        self.assertGreater(len(level_data.platforms), 0, "El nivel debe contener plataformas")
        self.assertGreater(len(level_data.enemies), 0, "El nivel debe contener enemigos")
        self.assertIsNotNone(level_data.goal_rect, "El nivel debe tener una meta")

        level_json_path = settings.LEVELS_DIR / "level_1.json"
        if level_json_path.exists():
            level_data_json = LevelLoader.load_level(level_json_path)
            self.assertIsNotNone(level_data_json.player)
            self.assertGreater(len(level_data_json.platforms), 0)

    def test_physics_gravity_and_ground_landing(self):
        """Verifica la aceleración por gravedad y el aterrizaje sobre una plataforma."""
        physics = PhysicsSystem(gravity=1.0)
        player = Player(x=100, y=100)
        platform = Platform(x=80, y=148, width=100, height=40)  # Ubicada justo debajo (player.height = 48)

        # Inicialmente en el aire
        self.assertFalse(player.is_grounded)
        self.assertEqual(player.vy, 0.0)

        # Actualizar física
        physics.update_player(player, [platform], [], dt=1.0)

        # Debe aterrizar en la plataforma
        self.assertTrue(player.is_grounded, "El jugador debe estar sobre el suelo tras el contacto")
        self.assertEqual(player.rect.bottom, platform.rect.top)
        self.assertEqual(player.vy, 0.0)

    def test_physics_stomp_enemy(self):
        """Verifica que al caer sobre la cabeza de un enemigo, este es derrotado y el jugador rebota."""
        physics = PhysicsSystem()
        player = Player(x=100, y=80)
        player.vy = 5.0  # Cayendo hacia abajo
        player.rect.bottom = 105

        enemy = Enemy(x=100, y=100)  # Su parte superior está en y=100

        defeated_enemies = []

        def on_stomp(e):
            defeated_enemies.append(e)

        physics.update_player(player, [], [enemy], dt=1.0, on_enemy_stomped=on_stomp)

        self.assertFalse(enemy.is_alive, "El enemigo debe ser derrotado al ser pisado")
        self.assertIn(enemy, defeated_enemies)
        self.assertLess(player.vy, 0.0, "El jugador debe rebotar hacia arriba tras pisar al enemigo")

    def test_scene_manager_lifecycle(self):
        """Verifica el flujo de cambio de escenas y entrega de parámetros."""
        sm = SceneManager()
        scene_a = DummyScene(sm)
        scene_b = DummyScene(sm)

        sm.register_scene("a", scene_a)
        sm.register_scene("b", scene_b)

        sm.change_scene("a")
        self.assertTrue(scene_a.entered)
        self.assertIs(sm.current_scene, scene_a)

        sm.change_scene("b", score=999)
        self.assertTrue(scene_a.exited)
        self.assertTrue(scene_b.entered)
        self.assertEqual(scene_b.received_data.get("score"), 999)


if __name__ == "__main__":
    unittest.main()
