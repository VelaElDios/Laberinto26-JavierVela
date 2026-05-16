"""
Módulo bicho.

Define la clase Bicho, los enemigos del laberinto.
"""
from ente import Ente


class Bicho(Ente):
    """
    Bicho representa a los enemigos del personaje.
    Su comportamiento varía según el Modo asignado (patrón State).
    """

    def __init__(self):
        super().__init__()
        self.modo = None

    def actua(self):
        """Delega la acción al modo actual del bicho."""
        if self.modo:
            self.modo.actua(self)

    def buscar_enemigo(self):
        """Pide al juego que le devuelva el personaje en su posición."""
        if self.juego:
            return self.juego.buscar_personaje(self)
        return None

    def es_agresivo(self):
        """Devuelve True si el modo actual es agresivo."""
        if self.modo:
            return self.modo.es_agresivo()
        return False

    def es_perezoso(self):
        """Devuelve True si el modo actual es perezoso."""
        if self.modo:
            return self.modo.es_perezoso()
        return False

    def muero(self):
        """Notifica al juego que el bicho ha muerto."""
        if self.juego:
            self.juego.muere_bicho(self)

    def obtener_orientacion_aleatoria(self):
        """Devuelve una orientación aleatoria de la posición actual."""
        if self.posicion:
            return self.posicion.obtener_orientacion_aleatoria()
        return None

    def __str__(self):
        modo_str = str(self.modo) if self.modo else "SinModo"
        return f"Bicho-{modo_str}"
