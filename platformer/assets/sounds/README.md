# Carpeta de Efectos de Sonido y Música

¡Aquí puedes darle vida a tu juego agregando música y efectos de audio!
(Se recomienda formato `.wav` u `.ogg` para efectos rápidos, y `.mp3` u `.ogg` para música de fondo).

Ideas de sonidos que puedes añadir:
- `jump.wav`: El sonido que suena cuando tu personaje salta.
- `hit.wav`: El sonido que suena cuando recibes daño o cuando aplastas a un enemigo.
- `win.wav`: Fanfarria de victoria cuando tocas la bandera de meta.
- `theme.ogg`: Música de fondo de tu nivel.

Cómo reproducir un sonido desde tu código:
```python
import pygame
import settings

# 1. Cargamos el archivo de sonido
sonido_salto = pygame.mixer.Sound(settings.SOUNDS_DIR / "jump.wav")

# 2. Lo reproducimos cuando quieras (por ejemplo, dentro del método jump())
sonido_salto.play()
```
