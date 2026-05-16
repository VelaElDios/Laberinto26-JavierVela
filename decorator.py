"""
Módulo decorator.

Define la clase Decorator, base del patrón Decorator para elementos
del mapa que envuelven a otro ElementoMapa.
"""
from hoja import Hoja


class Decorator(Hoja):
    """
    Decorator es una hoja que decora (envuelve) otro ElementoMapa.
    Implementa el patrón Decorator.
    """

    def __init__(self):
        super().__init__()
        self.em = None

    def entrar(self, alguien):
        """Delega la entrada al elemento decorado."""
        if self.em:
            self.em.entrar(alguien)
