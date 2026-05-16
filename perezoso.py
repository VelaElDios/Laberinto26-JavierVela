"""
Módulo perezoso.

Define la clase Perezoso, modo de bicho que actúa lentamente.
"""
import time
from modo import Modo


class Perezoso(Modo):
    """
    Perezoso es un modo del bicho que duerme mucho y actúa despacio.
    """

    def duerme(self, un_bicho):
        """Pausa de 3 segundos entre acciones."""
        print(f"{un_bicho} duerme")
        time.sleep(3)

    def es_perezoso(self):
        """Devuelve True."""
        return True

    def __str__(self):
        return "Perezoso"
