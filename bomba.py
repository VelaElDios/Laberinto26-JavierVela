"""
Módulo bomba.

Define la clase Bomba, un Decorator que puede explotar si está activa.
"""
from decorator import Decorator


class Bomba(Decorator):
    """
    Bomba es un elemento del mapa que puede explotar si está activa.
    Implementa el patrón Decorator añadiendo comportamiento explosivo.
    """

    def __init__(self):
        super().__init__()
        self.activa = False

    def activar(self):
        """Activa la bomba."""
        print("Bomba activada")
        self.activa = True

    def desactivar(self):
        """Desactiva la bomba."""
        print("Bomba desactivada")
        self.activa = False

    def entrar(self, alguien=None):
        """Explota si está activa y delega al elemento decorado."""
        if self.activa:
            if alguien:
                print(f"{alguien}, te ha explotado una bomba")
            else:
                print("Ha explotado una bomba")
        if self.em:
            self.em.entrar(alguien)

    def es_bomba(self):
        """Devuelve True."""
        return True
