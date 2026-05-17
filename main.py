"""Punto de entrada del juego del laberinto."""

import os
import sys
from director import Director, DirectorError
from Interfaz import InterfazTerminal


def main():
    """Lee el laberinto desde JSON, construye el juego y lanza la interfaz."""
    # Ruta al archivo JSON (junto al script)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_json = os.path.join(base_dir, "laberinto.json")

    try:
        director = Director()
        director.procesar(archivo_json)
    except DirectorError as exc:
        print(f"Error al construir el laberinto: {exc}")
        sys.exit(1)

    juego = director.obtener_juego()
    if not juego:
        print("Error: no se pudo obtener el juego del director.")
        sys.exit(1)

    # Abrir puertas y agregar personaje
    juego.abrir_puertas()
    juego.agregar_personaje("Hero")

    # Lanzar interfaz
    interfaz = InterfazTerminal(juego)
    interfaz.bucle_principal()


if __name__ == "__main__":
    main()
