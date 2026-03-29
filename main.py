"""Punto de entrada del juego del laberinto."""

from Juego import Juego
from Interfaz import InterfazTerminal


def main():
    """Inicializa un laberinto de 4 habitaciones y lanza la interfaz de terminal."""
    juego = Juego()
    juego.fabricar_lab4_hab_fm()
    juego.abrir_puertas()
    juego.agregar_personaje("Hero")

    interfaz = InterfazTerminal(juego)
    interfaz.bucle_principal()


if __name__ == "__main__":
    main()
