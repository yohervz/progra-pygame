"""
Clase base para tus Escenas (Scene Pattern).

¿Qué es una Escena?
Imagina que tu juego es una obra de teatro: cada pantalla es un "acto" distinto.
Por ejemplo:
1. La pantalla de Menú principal
2. La pantalla donde juegas tu nivel (PlayScene)
3. La pantalla de Fin de partida (GameOverScene)

Al separar tu juego en escenas, tu código se mantiene ordenado, limpio
y te resultará facilísimo añadir pantallas nuevas (como una tienda, créditos o pausa).
"""

from abc import ABC, abstractmethod
import pygame


class Scene(ABC):
    """
    Plantilla base para crear cualquiera de tus pantallas o escenas.
    
    ¡Para crear tu propia escena!:
    Crea una clase que herede de Scene (ejemplo: class MiTiendaScene(Scene))
    y completa los métodos principales: `handle_event`, `update` y `render`.
    """

    def __init__(self, manager) -> None:
        """
        Inicializa tu escena.
        
        :param manager: El SceneManager que te permitirá cambiar a otras escenas cuando quieras.
        """
        self.manager = manager

    def on_enter(self, **kwargs) -> None:
        """
        Este método se ejecuta automáticamente en el instante en que tu escena entra en pantalla.
        Úsalo para reiniciar la posición de tu personaje, resetear el puntaje
        o recibir datos que te envíe otra escena (por ejemplo, los puntos acumulados).
        """
        pass

    def on_exit(self) -> None:
        """
        Este método se ejecuta automáticamente justo cuando vas a salir de esta escena.
        Úsalo si necesitas detener música de fondo o guardar algún dato.
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Aquí procesas las acciones que realiza el jugador: teclas presionadas,
        movimientos del mouse o clics.
        
        :param event: Evento capturado por Pygame.
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Aquí colocas la lógica que cambia con el tiempo: mover a tus personajes,
        comprobar colisiones, actualizar temporizadores, etc.
        
        :param dt: Delta time (tiempo transcurrido para mantener la velocidad constante).
        """
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """
        Aquí dibujas todo lo visual de tu escena: fondos, plataformas, personajes y textos.
        
        :param surface: La superficie de la ventana donde debes dibujar.
        """
        pass
