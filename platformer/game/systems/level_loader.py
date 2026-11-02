"""
Cargador de Niveles (LevelLoader).

¡Aquí puedes diseñar tus propios niveles como un verdadero diseñador de videojuegos!
Puedes crear tu mapa en un simple archivo de texto (.txt) dibujándolo como una cuadrícula
o estructurándolo en un archivo .json.

Símbolos que puedes usar para diseñar tu nivel:
'#' -> Coloca una plataforma sólida
'P' -> Lugar donde aparece tu personaje al comenzar
'E' -> Coloca un enemigo patrullero
'G' -> Coloca la bandera de meta (¡al tocarla ganas!)
'.' -> Espacio vacío de aire

¡RETO PARA TI!:
¿Quieres monedas, trampas de pinchos o cofres?
¡Inventa un símbolo nuevo (ej: 'C' para monedas), agrégalo en el método `_parse_grid()`
y coloca monedas por todo tu mapa!
"""

import json
from pathlib import Path
from typing import List, Optional
import pygame

import settings
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.platform import Platform


class LevelData:
    """Guarda toda la información de tu nivel cargado."""

    def __init__(self) -> None:
        self.player: Optional[Player] = None
        self.player_spawn: tuple[float, float] = (100.0, 100.0)
        self.platforms: List[Platform] = []
        self.enemies: List[Enemy] = []
        self.goal_rect: Optional[pygame.Rect] = None
        self.width: int = settings.SCREEN_WIDTH
        self.height: int = settings.SCREEN_HEIGHT


class LevelLoader:
    """
    Lee tus archivos de mapas y construye automáticamente todos los objetos del juego.
    """

    @classmethod
    def load_level(cls, file_path: Path) -> LevelData:
        """
        Carga tu archivo de nivel reconociendo automáticamente si es .txt o .json.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de tu nivel: {path}")

        if path.suffix == ".json":
            return cls._load_from_json(path)
        else:
            return cls._load_from_txt(path)

    @classmethod
    def _load_from_txt(cls, path: Path) -> LevelData:
        """Lee tu archivo .txt línea por línea e ignora los comentarios que comiencen con //."""
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\r\n") for line in f if line.strip() != "" and not line.startswith("//")]

        return cls._parse_grid(lines)

    @classmethod
    def _load_from_json(cls, path: Path) -> LevelData:
        """Lee tu archivo .json y extrae la cuadrícula del mapa."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        grid = data.get("grid", [])
        return cls._parse_grid(grid)

    @classmethod
    def _parse_grid(cls, grid: List[str]) -> LevelData:
        """
        Recorre cada fila y columna de tu mapa y crea los objetos correspondientes.
        """
        level = LevelData()
        tile_size = settings.TILE_SIZE

        if not grid:
            return level

        max_cols = max(len(row) for row in grid)
        level.width = max_cols * tile_size
        level.height = len(grid) * tile_size

        for row_idx, row in enumerate(grid):
            for col_idx, char in enumerate(row):
                x = col_idx * tile_size
                y = row_idx * tile_size

                if char == "#":
                    # Creamos un bloque de plataforma sólida
                    plat = Platform(x=x, y=y, width=tile_size, height=tile_size)
                    level.platforms.append(plat)

                elif char == "P":
                    # Punto donde nace tu personaje
                    level.player_spawn = (float(x), float(y))
                    if level.player is None:
                        level.player = Player(x=x, y=y)

                elif char == "E":
                    # Colocamos un enemigo que patrullará esa zona
                    enemy = Enemy(x=x, y=y)
                    level.enemies.append(enemy)

                elif char == "G":
                    # Colocamos la bandera de meta
                    level.goal_rect = pygame.Rect(x, y, tile_size, tile_size)

        # Si olvidaste poner una 'P' en tu mapa, colocamos a tu personaje en una posición segura
        if level.player is None:
            level.player = Player(x=level.player_spawn[0], y=level.player_spawn[1])

        return level
