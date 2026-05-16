"""
Módulo pared_bomba.

Define la clase ParedBomba, variante de Pared usada por el patrón
Factory Method en JuegoBombas.
"""
from pared import Pared


class ParedBomba(Pared):
    """
    ParedBomba es una pared que tiene una bomba asociada.
    """

    def __init__(self):
        super().__init__()
        self.activa = False
