# ¡Bienvenido a tu Juego de Plataformas 2D en Pygame!

¡Hola! Esta es la base de tu nuevo videojuego de plataformas desarrollado con **Python** y **Pygame**.

La plantilla está diseñada para que puedas aprender, experimentar y construir tu juego a tu propio ritmo. No necesitas tener imágenes terminadas ni música desde el primer día: ¡el juego ya incluye figuras geométricas y colores por defecto para que puedas comenzar a programar mecánicas divertidas desde hoy mismo!

---

## 📁 Cómo está organizado tu proyecto

```text
platformer/
├── main.py                  # Punto de entrada (ejecuta este archivo para jugar)
├── settings.py              # ¡Tu panel de control! Gravedad, velocidad, resolución y colores
├── assets/
│   ├── images/              # Carpeta donde guardarás tus imágenes (player.png, platform.png, enemy.png)
│   ├── sounds/              # Carpeta donde guardarás tu música y efectos de sonido
│   └── levels/              # Tu mapa de juego (level_1.txt) diseñado en texto plano
├── game/
│   ├── core/
│   │   ├── game.py          # El corazón del motor: ventana, reloj y bucle principal
│   │   ├── scene.py         # La clase base para que crees tus propias pantallas
│   │   └── scene_manager.py # El director que te permite cambiar entre el Menú, Juego y Fin de Partida
│   ├── scenes/
│   │   ├── menu_scene.py    # Pantalla de bienvenida
│   │   ├── play_scene.py    # Pantalla donde juegas tu nivel activo
│   │   └── game_over_scene.py # Pantalla de victoria o Game Over
│   ├── entities/
│   │   ├── player.py        # Tu personaje principal (saltos, vidas y controles)
│   │   ├── enemy.py         # Enemigo patrullero que puedes derrotar saltando sobre él
│   │   └── platform.py      # Bloques sólidos sobre los que puedes pararte y caminar
│   ├── systems/
│   │   ├── physics.py       # La física de tu mundo: gravedad y detección de paredes/pisos
│   │   ├── camera.py        # Cámara 2D que te sigue suavemente por todo el nivel
│   │   └── level_loader.py  # Lee tu mapa de texto y crea todos los bloques automáticamente
│   └── ui/
│       └── hud.py           # Dibuja tus corazones de vida y tu puntaje fijo en pantalla
└── tests/
    └── test_platformer.py   # Pruebas automatizadas para comprobar que todo funcione bien
```

---

## 🚀 Cómo jugar y probar tu juego

### 1. Ejecutar el juego
Abre tu terminal y escribe:
```bash
python platformer/main.py
```
*(O entrando a la carpeta: `cd platformer` y luego `python main.py`)*

### 2. Ejecutar las pruebas unitarias
Para comprobar que la física, mapas y colisiones están respondiendo adecuadamente:
```bash
python platformer/tests/test_platformer.py
```

---

## 🎨 ¿Qué pasa si aún no tienes tus propios dibujos o sprites?

> **¡Tu juego nunca fallará por falta de imágenes!**

Cada objeto (`Player`, `Enemy`, `Platform`) cuenta con un **sistema de respaldo automático**:
1. El juego busca primero tus archivos en `assets/images/` (ej. `player.png`, `platform.png`, `enemy.png`).
2. Si el archivo **aún no existe**, el juego dibujará un personaje o bloque geométrico con colores atractivos, bordes y ojos que indican hacia dónde miras.
3. ¡Esto te permite concentrarte primero en programar la diversión y las mecánicas, y colocar tus propios dibujos cuando los tengas listos!

---

## 🗺️ Guía para personalizar tu juego paso a paso

Te recomendamos ir modificando tu juego en este orden:

### Paso 1: Personaliza las reglas en `settings.py`
- Prueba cambiar `PLAYER_SPEED` para correr más rápido.
- Modifica `PLAYER_JUMP_FORCE` para saltar más alto (recuerda que números negativos más grandes hacen que salte más hacia arriba, por ejemplo `-16.0`).
- Modifica `GRAVITY` para experimentar saltos pesados o saltos en gravedad cero.
- Cámbiale el color a tu fondo o a las vidas.

### Paso 2: Diseña tu propio nivel en `assets/levels/level_1.txt`
Abre ese archivo con cualquier editor de texto y diviértete dibujando tu mapa con caracteres:
- `#` = Bloque de suelo o pared
- `P` = Dónde naces tú al iniciar
- `E` = Coloca un enemigo patrullero
- `G` = Coloca la bandera dorada de Meta (¡tócala para ganar!)
- `.` = Espacio vacío de aire

### Paso 3: Agrega tu propio arte en `assets/images/`
- Agrega tu imagen `player.png` para vestir a tu personaje.
- Agrega `platform.png` para cambiar la textura de todos los bloques de tu mundo.
- Agrega `enemy.png` para crear tus propios villanos.

### Paso 4: Programa nuevas mecánicas
- **Doble salto**: Abre `game/entities/player.py` y agrega una variable que cuente tus saltos.
- **Monedas o tesoros**: Abre `game/systems/level_loader.py`, inventa un nuevo símbolo (como `'C'`) y dale puntos a tu personaje al tocarlo.
- **Plataformas móviles**: Abre `game/entities/platform.py` y dales movimiento en el método `update()`.

¡Mucho éxito creando tu videojuego!
