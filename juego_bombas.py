"""
Módulo juego_bombas.

Define la clase JuegoBombas, subclase de Juego que usa ParedBomba
como implementación del patrón Factory Method.
"""
from juego import Juego
from pared_bomba import ParedBomba


class JuegoBombas(Juego):
    """
    JuegoBombas ilustra el patrón Factory Method:
    sobreescribe fabricar_pared para devolver ParedBomba en lugar de Pared.
    """

    def fabricar_pared(self):
        """Crea y devuelve una ParedBomba en lugar de una Pared normal."""
        return ParedBomba()
