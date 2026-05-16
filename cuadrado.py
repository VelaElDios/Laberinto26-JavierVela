"""
Módulo cuadrado.

Define la clase Cuadrado, forma geométrica con cuatro orientaciones cardinales.
"""
from forma import Forma


class Cuadrado(Forma):
    """
    Cuadrado es un polígono regular de 4 lados con orientaciones
    norte, sur, este y oeste.
    """

    def __init__(self):
        super().__init__()
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
