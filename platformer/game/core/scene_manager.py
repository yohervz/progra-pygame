"""
Gestor de Escenas (Scene Manager).

Este componente es el "director" de tu juego: se encarga de cambiar de pantalla
de forma limpia (por ejemplo, cuando pasas del Menú al Juego, o del Juego a Game Over).

Tú solo tienes que pedirle: `self.manager.change_scene("play")` y él se encarga
de apagar la pantalla anterior y encender la nueva.
"""

from typing import Dict, Optional
import pygame
from game.core.scene import Scene


class SceneManager:
    """
    Controlador central donde registras tus pantallas y navegas entre ellas.
    """

    def __init__(self) -> None:
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None
        self.current_scene_name: Optional[str] = None

    def register_scene(self, name: str, scene: Scene) -> None:
        """
        Registra una de tus escenas dándole un nombre para identificarla.
        
        :param name: El nombre que tú elijas (ejemplo: 'menu', 'play', 'tienda', 'game_over').
        :param scene: La instancia de la escena que creaste.
        """
        self.scenes[name] = scene

    def change_scene(self, name: str, **kwargs) -> None:
        """
        Cambia la pantalla visible por la que tú le indiques.
        
        Puedes pasarle datos adicionales si lo necesitas:
        Ejemplo: `self.manager.change_scene("game_over", victory=True, score=self.score)`
        
        :param name: El nombre de la escena a la que quieres viajar.
        :param kwargs: Cualquier dato extra que quieras enviarle a la nueva escena.
        """
        if name not in self.scenes:
            raise KeyError(f"La escena '{name}' no está registrada. Asegúrate de registrarla primero con register_scene().")

        # Le avisamos a la escena previa que vamos a salir de ella
        if self.current_scene is not None:
            self.current_scene.on_exit()

        # Activamos la nueva escena y le enviamos tus datos
        self.current_scene_name = name
        self.current_scene = self.scenes[name]
        self.current_scene.on_enter(**kwargs)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Envía el evento de teclado/mouse a la escena que tengas activa en este momento."""
        if self.current_scene is not None:
            self.current_scene.handle_event(event)

    def update(self, dt: float) -> None:
        """Actualiza la lógica de la escena que tengas activa en este momento."""
        if self.current_scene is not None:
            self.current_scene.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        """Dibuja en pantalla la escena que tengas activa en este momento."""
        if self.current_scene is not None:
            self.current_scene.render(surface)
