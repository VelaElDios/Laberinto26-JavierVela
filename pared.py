"""
Módulo pared.

Define la clase Pared, elemento simple impasable del laberinto.
"""
from hoja import Hoja


class Pared(Hoja):
    """
    Pared es un elemento del mapa que no se puede atravesar.
    """

    def entrar(self, alguien):
        """Informa de que se ha chocado contra una pared."""
        msg = "¡Chocaste con una pared!"
        if alguien and hasattr(alguien, 'ultimo_evento'):
            alguien.ultimo_evento = msg
        else:
            print(msg)

    def __str__(self):
        return "Pared"
