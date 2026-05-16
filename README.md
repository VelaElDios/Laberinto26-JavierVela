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

Usa las teclas **N / S / E / O** para mover al personaje y **Q** para salir.

---

## Estructura del proyecto

```
laberinto26-Python/
│
├── main.py               # Punto de entrada
│
│── orientacion.py        # Clase base abstracta Orientacion (Singleton)
├── norte.py              # Orientación Norte
├── sur.py                # Orientación Sur
├── este.py               # Orientación Este
├── oeste.py              # Orientación Oeste
├── noreste.py            # Orientación Noreste (Rombo)
├── noroeste.py           # Orientación Noroeste (Rombo)
├── sureste.py            # Orientación Sureste  (Rombo)
├── suroeste.py           # Orientación Suroeste (Rombo)
├── Orientaciones.py      # Módulo de compatibilidad (reexporta todo lo anterior)
│
├── ElementosMapa.py      # Jerarquía Composite: ElementoMapa, Hoja, Contenedor,
│                         #   Pared, ParedBomba, Habitacion, Laberinto, Puerta, Armario
├── Formas.py             # Formas geométricas: Cuadrado, Rombo
├── Decoradores.py        # Patrón Decorator: Bomba
├── Entes.py              # Personaje y Bicho
├── Modos.py              # Estados del Bicho: Agresivo, Perezoso (patrón State)
├── Juego.py              # Clase Juego (Factory Method) y JuegoBombas
├── Builders.py           # Patrón Builder: LaberintoBuilder, LaberintoBuilderRombo, Director
└── Interfaz.py           # Interfaz de terminal para el juego
```

---

## Patrones de diseño implementados

| Patrón | Descripción | Ubicación en el código |
|---|---|---|
| **Singleton** | Garantiza una única instancia por cada subclase de `Orientacion` | `orientacion.py` → `Orientacion.__new__` + `Orientacion.default()` |
| **Composite** | Los elementos del mapa se componen en árbol (Laberinto → Habitacion → …) | `ElementosMapa.py` → `ElementoMapa`, `Hoja`, `Contenedor` |
| **Decorator** | Añade comportamiento de bomba a una pared sin modificar su clase | `Decoradores.py` → `Decorator`, `Bomba` |
| **Builder** | Construye el laberinto paso a paso a partir de un fichero JSON | `Builders.py` → `LaberintoBuilder`, `LaberintoBuilderRombo`, `Director` |
| **Factory Method** | `Juego` y `JuegoBombas` sobreescriben métodos `fabricar_*` para crear variantes | `Juego.py` → `Juego`, `JuegoBombas` |
| **State** | El comportamiento del `Bicho` varía según su modo activo | `Modos.py` → `Agresivo`, `Perezoso` |

---

## Explicación del patrón Singleton en `Orientacion`

Las orientaciones (`Norte`, `Sur`, `Este`, `Oeste`, …) son objetos sin estado propio: no tiene sentido crear más de una instancia de cada una.

El Singleton está implementado directamente en la clase base `Orientacion` mediante:

- **`__new__`**: intercepta toda creación de instancia y la almacena en el diccionario `Orientacion._instancias`, indexado por subclase.
- **`default()`**: método de clase que devuelve la instancia única de la subclase concreta que lo invoca (`Norte.default()`, `Sur.default()`, etc.).

```python
# Ejemplo de uso
norte1 = Norte.default()
norte2 = Norte.default()
assert norte1 is norte2          # True → misma instancia
assert norte1 is Sur.default()   # False → instancias distintas por subclase
```
