"""
Módulo rombo.

Define la clase Rombo, forma geométrica con cuatro orientaciones diagonales.
"""
from forma import Forma


class Rombo(Forma):
    """
    Rombo es un polígono con orientaciones noreste (ne), noroeste (no),
    sureste (se) y suroeste (so).
    """

    def __init__(self):
        super().__init__()
        self.ne = None
        self.no = None
        self.se = None
        self.so = None
