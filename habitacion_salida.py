"""
Módulo habitacion_salida.

Define la clase HabitacionSalida, habitación especial que marca
la victoria del personaje al entrar en ella.
"""
from habitacion import Habitacion


class HabitacionSalida(Habitacion):
    """
    HabitacionSalida es la habitación de salida del laberinto.
    Cuando el personaje entra, gana la partida.
    """

    def entrar(self, alguien):
        """Hace entrar a alguien; si es el personaje, gana la partida."""
        alguien.posicion = self
        msg = f"¡Has llegado a la SALIDA ({self})!"
        if hasattr(alguien, 'ultimo_evento'):
            alguien.ultimo_evento = msg
        # Notifica al juego que el personaje ha ganado
        if hasattr(alguien, 'nombre') and alguien.juego:
            alguien.juego.gana_personaje()

    def es_salida(self):
        """Devuelve True para identificar esta habitación como la salida."""
        return True

    def __str__(self):
        return f"SALIDA-{self.num}"
