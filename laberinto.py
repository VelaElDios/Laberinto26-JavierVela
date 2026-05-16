"""
Módulo laberinto.

Define la clase Laberinto, contenedor raíz que agrupa habitaciones.
"""
from contenedor import Contenedor


class Laberinto(Contenedor):
    """
    Laberinto es el contenedor raíz que agrupa todas las habitaciones.
    """

    def agregar_habitacion(self, una_hab):
        """Añade una habitación al laberinto."""
        self.agregar_hijo(una_hab)

    def entrar(self, alguien):
        """Hace entrar a alguien en la primera habitación del laberinto."""
        hab = self.obtener_habitacion(1)
        if hab:
            hab.entrar(alguien)

    def obtener_habitacion(self, un_num):
        """Devuelve la habitación con el número indicado, o None."""
        for hijo in self.hijos:
            if getattr(hijo, 'num', None) == un_num:
                return hijo
        return None

    def recorrer(self, un_bloque):
        """Recorre todas las habitaciones del laberinto."""
        print("Recorriendo el laberinto")
        for hijo in self.hijos:
            hijo.recorrer(un_bloque)
