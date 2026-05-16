"""
Módulo habitacion.

Define la clase Habitacion, contenedor principal del laberinto
en el que habitan los entes.
"""
from contenedor import Contenedor


class Habitacion(Contenedor):
    """
    Habitacion es un contenedor en el que pueden entrar los entes.
    """

    def entrar(self, alguien):
        """Hace entrar a alguien en esta habitación."""
        alguien.posicion = self
        msg = f"Has entrado en {self}."
        if hasattr(alguien, 'ultimo_evento'):
            alguien.ultimo_evento = msg
        else:
            print(f"{alguien} está en {self}")

    def __str__(self):
        return f"Hab-{self.num}"
