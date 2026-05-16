# Laberinto26 – Javier Vela

Proyecto de Diseño de Software — 2.º Cuatrimestre IGF.

Implementación en Python de un juego de laberinto basado en el proyecto original en Smalltalk (Pharo).
El objetivo del proyecto es poner en práctica los patrones de diseño GoF estudiados en clase, manteniendo la arquitectura original del sistema.

---

## Instrucciones para ejecutar

Requiere **Python 3.10+** y no tiene dependencias externas.

```bash
python main.py
```

Usa las teclas **W / S / A / D** o las **flechas del teclado** para mover al personaje y **Q** para salir.

---

## Estructura del proyecto

Cada clase tiene su propio archivo, siguiendo la misma organización que el proyecto original en Pharo (un `.class.st` por clase).

```
laberinto26-Python/
│
├── main.py                      # Punto de entrada
├── Interfaz.py                  # Interfaz de terminal (visualización ASCII + input)
│
│── # ── Patrón Composite: jerarquía de elementos del mapa ──────────────────
├── elemento_mapa.py             # Clase base ElementoMapa
├── hoja.py                      # Leaf del Composite
├── contenedor.py                # Composite del Composite
├── pared.py                     # Hoja concreta: Pared
├── pared_bomba.py               # Hoja concreta: ParedBomba (usada por Factory Method)
├── puerta.py                    # Hoja concreta: Puerta (abierta/cerrada)
├── habitacion.py                # Contenedor concreto: Habitacion
├── laberinto.py                 # Contenedor raíz: Laberinto
├── armario.py                   # Contenedor secundario: Armario
│
│── # ── Patrón Bridge: formas geométricas ─────────────────────────────────
├── forma.py                     # Abstracción: Forma
├── cuadrado.py                  # Implementación concreta: Cuadrado (N/S/E/O)
├── rombo.py                     # Implementación concreta: Rombo  (NE/NO/SE/SO)
│
│── # ── Patrón Singleton: orientaciones ───────────────────────────────────
├── orientacion.py               # Clase base Orientacion → Singleton aquí
├── norte.py                     # Norte  (una sola instancia global)
├── sur.py                       # Sur
├── este.py                      # Este
├── oeste.py                     # Oeste
├── noreste.py                   # Noreste  (para Rombo)
├── noroeste.py                  # Noroeste
├── sureste.py                   # Sureste
├── suroeste.py                  # Suroeste
│
│── # ── Patrón Decorator ───────────────────────────────────────────────────
├── decorator.py                 # Clase base Decorator
├── bomba.py                     # Bomba: Decorator concreto
│
│── # ── Entes ──────────────────────────────────────────────────────────────
├── ente.py                      # Clase base Ente
├── personaje.py                 # Personaje (controlado por el jugador)
├── bicho.py                     # Bicho (enemigo autónomo)
│
│── # ── Patrón State: modos de los bichos ─────────────────────────────────
├── modo.py                      # Interfaz Modo
├── agresivo.py                  # Estado Agresivo (actúa cada 1 s)
├── perezoso.py                  # Estado Perezoso (actúa cada 3 s)
│
│── # ── Patrón Factory Method ──────────────────────────────────────────────
├── juego.py                     # Juego: métodos fabricar_* sobreescribibles
├── juego_bombas.py              # JuegoBombas: sobreescribe fabricar_pared()
│
└── # ── Patrón Builder ─────────────────────────────────────────────────────
    ├── laberinto_builder.py         # ConcreteBuilder (laberinto cuadrado)
    ├── laberinto_builder_rombo.py   # ConcreteBuilder (laberinto rombo)
    └── director.py                  # Director: lee JSON y dirige la construcción
```

---

## Patrones de diseño implementados

| Patrón | Dónde se aplica | Clases principales |
|---|---|---|
| **Singleton** | Las orientaciones son únicas en todo el programa | `orientacion.py` → `Orientacion.__new__` + `default()` |
| **Composite** | Los elementos del mapa se componen en árbol | `elemento_mapa.py`, `hoja.py`, `contenedor.py` |
| **Bridge** | Desacopla la forma geométrica del contenedor | `forma.py`, `cuadrado.py`, `rombo.py` |
| **Decorator** | Añade comportamiento de bomba sin modificar la clase | `decorator.py`, `bomba.py` |
| **Builder** | Construye el laberinto paso a paso desde un JSON | `laberinto_builder.py`, `director.py` |
| **Factory Method** | `Juego` expone métodos `fabricar_*` sobreescribibles | `juego.py`, `juego_bombas.py` |
| **State** | El comportamiento del `Bicho` cambia según su modo | `modo.py`, `agresivo.py`, `perezoso.py` |

### 🔍 El Singleton en `Orientacion`

Las orientaciones (`Norte`, `Sur`, etc.) no tienen estado propio, así que no tiene sentido crear más de una instancia de cada una. El patrón está implementado **directamente en la clase base `Orientacion`**:

- `_instancias` — diccionario que guarda una instancia por subclase.
- `__new__` — intercepta toda creación y garantiza que solo existe una.
- `default()` — método de clase para obtener la instancia única.

```python
norte1 = Norte.default()
norte2 = Norte.default()
assert norte1 is norte2           # ✅ misma instancia
assert norte1 is not Sur.default() # ✅ instancias distintas por subclase
```
