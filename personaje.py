"""
Módulo personaje.

Define la clase Personaje, el protagonista controlado por el jugador.
"""
from ente import Ente


class Personaje(Ente):
    """
    Personaje es el protagonista del juego, controlado por el jugador.
    """

    def __init__(self):
        super().__init__()
        self.nombre = ""
        self.ultimo_evento = ""

    def buscar_enemigo(self):
        """El personaje no busca enemigos activamente."""
        return None

    def ir_a(self, una_or):
        """Mueve al personaje en la dirección indicada por una_or."""
        una_or.caminar(self)

    def ir_al_norte(self):
        """Mueve al personaje hacia el norte de su posición actual."""
        if self.posicion:
            self.posicion.ir_al_norte(self)

    def muero(self):
        """Notifica al juego que el personaje ha muerto."""
        if self.juego:
            self.juego.muere_personaje()

    def __str__(self):
        return self.nombre
