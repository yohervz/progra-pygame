"""
¡Bienvenido/a a la configuración de tu juego de plataformas!

En este archivo puedes personalizar todas las constantes y reglas generales
de tu mundo: la gravedad, la velocidad a la que corre tu personaje, la fuerza
de su salto, los colores de fondo y la resolución de la pantalla.

¡Prueba cambiar algunos números y ejecuta el juego para ver cómo cambia!
"""

from pathlib import Path
import pygame

# ==========================================
# 1. RUTAS DE TUS RECURSOS (Assets)
# ==========================================
# Aquí indicamos dónde están guardadas tus imágenes, sonidos y mapas.
# 'BASE_DIR' detecta automáticamente la carpeta raíz de tu juego.
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
LEVELS_DIR = ASSETS_DIR / "levels"

# ==========================================
# 2. CONFIGURACIÓN DE TU VENTANA
# ==========================================
# ¡Cámbiale el título a tu juego!
WINDOW_TITLE = "Mi Juego de Plataformas 2D"

# Tamaño de la ventana en píxeles (ancho y alto)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cuántos fotogramas por segundo quieres que corra tu juego (60 es el estándar fluido)
FPS = 60

# Tamaño de cada bloque de plataforma en tu mapa (en píxeles)
# Si tus bloques miden 40x40, un mapa de 20 bloques de ancho medirá 800px.
TILE_SIZE = 40

# ==========================================
# 3. FÍSICA Y MOVIMIENTO DE TU JUEGO
# ==========================================
# Fuerza con la que el mundo jala hacia abajo a las entidades cada fotograma.
# Prueba aumentarla a 1.2 si quieres que caiga más rápido, o bajarla a 0.4 para un salto lunar.
GRAVITY = 0.8

# Velocidad máxima de caída para evitar que tu personaje caiga tan rápido que traspase pisos.
MAX_FALL_SPEED = 14.0

# --- Parámetros de tu Jugador ---
# Velocidad al caminar hacia los lados (píxeles por fotograma)
PLAYER_SPEED = 5.0

# Impulso hacia arriba al presionar saltar (en Pygame, los valores negativos van hacia ARRIBA)
# Si quieres que salte más alto, prueba con -16.0 o -18.0.
PLAYER_JUMP_FORCE = -14.0

# Cantidad de vidas o puntos de salud con los que inicias la partida
PLAYER_MAX_HEALTH = 3

# --- Parámetros de tus Enemigos ---
# Velocidad a la que patrullan los enemigos de tu nivel
ENEMY_SPEED = 2.0

# ==========================================
# 4. PALETA DE COLORES (Formato RGB: Rojo, Verde, Azul)
# ==========================================
# Puedes inventar tus propios colores combinando valores de 0 a 255.
COLOR_BLACK = (20, 20, 25)
COLOR_WHITE = (245, 245, 245)
COLOR_BACKGROUND = (30, 35, 45)       # Color de fondo si no usas una imagen de cielo
COLOR_GRID = (45, 50, 65)

# Colores de respaldo: Si aún no dibujas o no descargas tus imágenes en assets/images/,
# tu juego utilizará automáticamente estos colores para dibujar a tus personajes y bloques.
COLOR_FALLBACK_PLAYER = (52, 152, 219)     # Azul cielo para tu personaje
COLOR_FALLBACK_ENEMY = (231, 76, 60)       # Rojo para los enemigos
COLOR_FALLBACK_PLATFORM = (46, 204, 113)   # Verde esmeralda para tus plataformas
COLOR_FALLBACK_COIN = (241, 196, 15)       # Amarillo dorado para la meta o monedas
COLOR_TEXT = (236, 240, 241)               # Color de las letras del HUD y menús
COLOR_ACCENT = (155, 89, 182)             # Color secundario
COLOR_HEALTH = (231, 76, 60)               # Color de tus corazones / vidas
