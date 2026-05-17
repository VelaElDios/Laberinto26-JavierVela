# Laberinto26 - Javier Vela

## Descripcion

Proyecto de **Diseño de Software** que implementa un laberinto interactivo en Python usando múltiples **patrones de diseño**. El jugador debe escapar del laberinto enfrentándose a entes, desactivando bombas, comerciando con vendedores y sobreviviendo a trampas con temporizador, todo desde una interfaz ASCII en terminal.

## Ejecucion

```bash
python main.py
```

## Menu Principal

Al iniciar el juego aparece un menu con 4 opciones:

| Tecla | Opcion | Descripcion |
|-------|--------|-------------|
| `1` | **Jugar** | Inicia la partida con la config seleccionada |
| `2` | **Dificultad** | Elige Normal o Dificil |
| `3` | **Clase** | Elige Alumno, Guerrero o Profesor |
| `4` | **Salir** | Cierra el juego |

### Dificultad

| Modo | Vidas base | En niebla (PPT) |
|------|-----------|------------------|
| **Normal** | 3 | 2 |
| **Dificil** | 2 | 1 |

### Clases

| Clase | Habilidad especial | Tiempo |
|-------|-------------------|--------|
| **Alumno** | Ninguna (clase basica) | +50% (x1.5) |
| **Guerrero** | Puede comprar **Espada** en tienda (3 sangre). Con espada, auto-gana combates contra entes | -25% (x0.75) |
| **Profesor** | Las bombas se desactivan automaticamente (no hace falta Simon Dice) | Normal (x1.0) |

El multiplicador de tiempo afecta a: temporizadores de sala, timer global del laberinto, y tiempo limite de eventos (combate/bomba).

## Controles

| Tecla | Accion |
|-------|--------|
| `W` / `↑` | Mover al Norte |
| `S` / `↓` | Mover al Sur |
| `A` / `←` | Mover al Oeste |
| `D` / `→` | Mover al Este |
| `Q` | Salir del juego |
| `R/P/T` | Piedra/Papel/Tijeras (en combate) |
| `W/A/S/D` | Secuencia Simon Dice (en bomba) |
| `C` | Comprar en tienda |
| `E` | Comprar Espada (guerrero, en tienda) |
| `Q` | Salir de tienda |

## Configuracion (laberinto.json)

El laberinto se define en `laberinto.json` con la siguiente estructura:

```json
{
    "forma": "poligono4",
    "laberinto": [
        {"tipo": "habitacion", "num": 1},
        {"tipo": "habitacion_salida", "num": 5},
        {"tipo": "habitacion_tienda", "num": 6}
    ],
    "puertas": [[1, "sur", 2, "norte"]],
    "bichos": [{"modo": "agresivo", "posicion": 3}],
    "bombas": [2],
    "nieblas": [3],
    "mimicos": [2],
    "temporizadores": [{"habitacion": 3, "segundos": 60}],
    "timer_global": 300
}
```

### Tipos de habitacion
- `habitacion` — Sala normal
- `habitacion_salida` — Meta del juego (llegar aqui = victoria)
- `habitacion_tienda` — Sala con vendedor (comprar vidas con sangre)
- `armario` — Contenedor dentro de una habitacion

### Tipos de bicho
- `agresivo` — Ataca al jugador (evento Piedra-Papel-Tijeras)
- `perezoso` — Comerciante ambulante (vende vidas por sangre)

### Decoradores
- `bombas` — Lista de habitaciones con bomba (evento Simon Dice)
- `nieblas` — Lista de habitaciones con niebla (oculta salidas)
- `mimicos` — Lista de habitaciones con mimico (invierte reglas)
- `temporizadores` — Lista de `{habitacion, segundos}` con limite de tiempo

---

## Patrones de Diseño

### 1. Composite
**Clases:** `ElementoMapa`, `Contenedor`, `Hoja`

El laberinto es un arbol Composite donde cada elemento (`Habitacion`, `Puerta`, `Pared`, `Armario`, `Laberinto`) se trata de forma uniforme a traves de la interfaz `ElementoMapa`. Los `Contenedor`es pueden tener hijos (`agregar_hijo`, `recorrer`), mientras que las `Hoja`s son elementos terminales.

```
ElementoMapa (Component)
├── Hoja (Leaf): Pared, Puerta
└── Contenedor (Composite): Habitacion, Armario, Laberinto
```

### 2. Decorator
**Clases:** `Decorator`, `Bomba`, `Niebla`, `Mimico`, `Temporizador`

Los decoradores añaden comportamiento a las habitaciones sin modificar su código. Se implementan como hijos del Composite, envolviendo el elemento decorado.

| Decorador | Efecto |
|-----------|--------|
| **Bomba** | Activa evento Simon Dice al entrar |
| **Niebla** | Oculta salidas, +dificultad (2 vidas PPT / 1 en dificil, 4 teclas Simon) |
| **Mimico** | Invierte reglas (PPT invertido, controles Simon invertidos) |
| **Temporizador** | Limite de tiempo segun clase: 60s*mult sala, 20s*mult eventos, 300s*mult global |

### 3. Builder
**Clases:** `LaberintoBuilder`, `LaberintoBuilderRombo`, `Director`

El `Director` lee la configuración JSON y delega la construcción al `Builder` concreto. El `LaberintoBuilder` crea habitaciones cuadradas, puertas, paredes, bombas, nieblas, mimicos, temporizadores, bichos y tiendas.

```
Director.procesar(archivo) → Builder.fabricar_*() → Laberinto completo
```

### 4. Factory Method
**Clases:** `Juego`, `JuegoBombas`, `JuegoNiebla`, `JuegoTiempo`

Cada subclase de `Juego` sobreescribe `fabricar_habitacion_num()` para añadir decoradores automaticamente a todas las habitaciones:

| Clase | Decorador por defecto |
|-------|----------------------|
| `Juego` | Ninguno |
| `JuegoBombas` | Bomba en todas las habitaciones |
| `JuegoNiebla` | Niebla en todas las habitaciones |
| `JuegoTiempo` | Temporizador(60s) en todas las habitaciones |

### 5. Singleton
**Clases:** `Norte`, `Sur`, `Este`, `Oeste`, `Noreste`, `Noroeste`, `Sureste`, `Suroeste`

Las orientaciones cardinales usan Singleton (`default()`) para asegurar una unica instancia por direccion.

### 6. State
**Clases:** `Modo`, `Agresivo`, `Perezoso`

Los bichos tienen un `Modo` (State) que determina su comportamiento:
- **Agresivo:** Busca y ataca al jugador → evento PPT
- **Perezoso:** Ofrece comercio → evento Tienda

---

## Mecanicas de Juego

### Combate: Piedra-Papel-Tijeras (PPT)
- **Normal:** Jugador 3 vidas, Ente 1 vida
- **Dificil:** Jugador 2 vidas, Ente 1 vida
- **En niebla (normal):** Jugador 2 vidas
- **En niebla (dificil):** Jugador 1 vida
- **Mimico:** Reglas invertidas (Tijera>Piedra, Piedra>Papel, Papel>Tijera)
- **Con temporizador:** 20s * mult_clase para completar el combate
- **Guerrero con Espada:** Auto-gana (no hay minijuego)

### Bomba: Simon Dice
- **Normal:** Secuencia de 3 teclas WASD
- **En niebla:** Secuencia de 4 teclas
- **Mimico:** Controles invertidos (W↔S, A↔D)
- **Con temporizador:** 20s * mult_clase para desactivar
- **Profesor:** Auto-desactiva (no hay minijuego)

### Sistema de Sangre
- **Obtencion:** +1 sangre al derrotar un ente agresivo
- **Uso:** Comprar vidas en tiendas (2 sangre = 1 vida) o Espada (3 sangre, solo guerrero)

### Tiendas
- **Habitacion Tienda:** Sala con vendedor fijo
- **Ente Perezoso:** Comerciante ambulante (misma mecanica)
- **Inventario:** [C] Comprar vida, [E] Comprar Espada (solo guerrero), [Q] Salir

### Espada (Guerrero)
- Se compra en cualquier tienda por 3 sangre
- Mientras se tiene, todos los combates contra entes se ganan automaticamente
- Se muestra en la barra de stats como `Equip: ESPADA`

### Temporizadores
- **Sala con temporizador:** 60s * mult_clase para salir o los pinchos bajan (-1 vida)
- **Eventos temporizados:** 20s * mult_clase para completar combate/bomba
- **Timer global:** 300s * mult_clase para completar el laberinto o se cierran las puertas

| Clase | Sala (base 60s) | Evento (base 20s) | Global (base 300s) |
|-------|-----------------|-------------------|-------------------|
| Alumno | 90s | 30s | 450s (7.5 min) |
| Guerrero | 45s | 15s | 225s (3.75 min) |
| Profesor | 60s | 20s | 300s (5 min) |

### Niebla
- Las salidas se muestran como `[ ??? ]`
- No se ve hacia donde llevan las puertas
- Aumenta dificultad de combate y bombas

---

## Interfaz

La interfaz muestra:
- **Titulo:** Nombre de la sala y tipo
- **Stats:** Vidas, sangre, timer global
- **Info:** Clase, dificultad, equipamiento
- **Indicadores:** Niebla, mimico, entes, bombas, tienda, timer de sala
- **Mapa:** Norte/Sur/Este/Oeste (oculto en niebla)
- **Evento:** Ultimo evento (2 lineas)
- **Controles:** WASD/flechas

---

## Estructura del Proyecto

```
Laberinto26-Phyton/
├── main.py                 # Punto de entrada
├── laberinto.json          # Configuracion del laberinto
├── Interfaz.py             # Menu + Interfaz ASCII + minijuegos
├── evento.py               # EventoPPT, EventoSimonDice, EventoTienda
│
├── elemento_mapa.py        # Component (Composite)
├── contenedor.py           # Composite
├── hoja.py                 # Leaf
├── habitacion.py           # Habitacion normal
├── habitacion_salida.py    # Habitacion de salida (victoria)
├── habitacion_tienda.py    # Habitacion con vendedor
├── laberinto.py            # Laberinto (Composite raiz)
├── armario.py              # Armario (Composite)
├── pared.py                # Pared (Leaf)
├── puerta.py               # Puerta (Leaf)
│
├── decorator.py            # Decorator base
├── bomba.py                # Decorator Bomba
├── niebla.py               # Decorator Niebla
├── mimico.py               # Decorator Mimico
├── temporizador.py         # Decorator Temporizador
│
├── juego.py                # Juego base
├── juego_bombas.py         # Factory Method: laberinto con bombas
├── juego_niebla.py         # Factory Method: laberinto con niebla
├── juego_tiempo.py         # Factory Method: laberinto del tiempo
│
├── director.py             # Director (Builder pattern)
├── laberinto_builder.py    # ConcreteBuilder cuadrado
├── laberinto_builder_rombo.py  # ConcreteBuilder rombo
│
├── forma.py                # Forma base
├── cuadrado.py             # Forma cuadrada (4 orientaciones)
├── rombo.py                # Forma rombo (8 orientaciones)
│
├── orientacion.py          # Orientacion base (Singleton)
├── norte.py / sur.py       # Orientaciones cardinales
├── este.py / oeste.py      # Orientaciones cardinales
├── noreste.py / noroeste.py    # Orientaciones diagonales
├── sureste.py / suroeste.py    # Orientaciones diagonales
│
├── ente.py                 # Ente base
├── personaje.py            # Personaje (jugador: clase, dificultad, espada)
├── bicho.py                # Bicho (enemigo)
├── modo.py                 # State base
├── agresivo.py             # State: modo agresivo
└── perezoso.py             # State: modo perezoso
```

---

## Diagrama de Clases
<p align="center">
  <img src="https://github.com/user-attachments/assets/ec7db516-0e46-4985-a041-8a64bd278f00" width="800" alt="Diagrama de Clases">
</p>


## Diagrama de Secuencia de Combate
<p align="center">
  <img src="https://github.com/user-attachments/assets/5a2deeae-60f6-4b4d-b773-0dcc2a0e84f2" width="600" alt="Diagrama de Secuencia - Combate">
</p>


## Diagrama de Secuencia de Bomba
<p align="center">
  <img src="https://github.com/user-attachments/assets/32c562de-07c3-4204-9358-f7d1d0108c7e" width="600" alt="Diagrama de Secuencia - Bomba">
</p>




## Mapa del Laberinto por Defecto

```
Hab-1 ═══[puerta]═══ Hab-3 [NIEBLA+TIMER+Agresivo]
  ║                    ║
[puerta]            [puerta]
  ║                    ║
Hab-2 ═══[puerta]═══ Hab-4 ═══[puerta]═══ TIENDA-6 ═══[puerta]═══ SALIDA-5
[MIMICO+BOMBA]     [TIMER+Perezoso]       [Vendedor]
```

**Modificadores activos:**
- Hab-2: Mimico (Simon Dice invertido) + Bomba
- Hab-3: Niebla (salidas ocultas, vidas reducidas) + Temporizador (60s) + Ente Agresivo
- Hab-4: Temporizador (60s) + Ente Perezoso (tienda ambulante)
- Hab-6: Tienda fija (vendedor) — donde el Guerrero puede comprar Espada
- Timer Global: 300s (ajustado segun clase)

---

## Autor

**Javier Vela** — Grado en Ingenieria y Gestion del Videojuego (IGF)
Asignatura: Diseño de Software — Segundo Cuatrimestre
