"""
Módulo agresivo.

Define la clase Agresivo, modo de bicho que actúa con rapidez.
"""
import time
from modo import Modo


class Agresivo(Modo):
    """
    Agresivo es un modo del bicho que duerme poco y actúa con rapidez.
    """

    def duerme(self, un_bicho):
        """Pausa de 1 segundo entre acciones."""
        print(f"{un_bicho} duerme")
        time.sleep(1)

    def es_agresivo(self):
        """Devuelve True."""
        return True

    def __str__(self):
        return "Agresivo"
