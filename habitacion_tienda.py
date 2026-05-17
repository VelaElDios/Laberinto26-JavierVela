"""
Modulo habitacion_tienda.

Define la clase HabitacionTienda, habitacion especial con un vendedor
que permite comprar vidas a cambio de sangre.
"""
from habitacion import Habitacion


class HabitacionTienda(Habitacion):
    """
    HabitacionTienda es una habitacion con un vendedor.
    El personaje puede comprar vidas a cambio de sangre.
    """

    def __init__(self):
        super().__init__()
        self.precio_vida = 2   # sangre necesaria para 1 vida

    def entrar(self, alguien):
        """Hace entrar a alguien; informa de la tienda."""
        alguien.posicion = self
        msg = f"Has entrado en la TIENDA ({self}). Hay un vendedor."
        if hasattr(alguien, 'ultimo_evento'):
            alguien.ultimo_evento = msg
        else:
            print(f"{alguien} entra en tienda")

    def es_tienda(self):
        """Devuelve True para identificar esta habitacion como tienda."""
        return True

    def __str__(self):
        return f"TIENDA-{self.num}"
