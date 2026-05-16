"""
Módulo ente.

Define la clase base Ente, interfaz de los elementos autónomos del laberinto.
"""


class Ente:
    """
    Ente es la interfaz de los elementos autónomos del laberinto
    (personajes y bichos).
    """

    def __init__(self):
        self.poder = 1
        self.posicion = None
        self.vidas = 50
        self.juego = None

    def atacar(self):
        """Ataca al enemigo si hay uno disponible."""
        enemigo = self.buscar_enemigo()
        if enemigo:
            enemigo.es_atacado_por(self)

    def buscar_enemigo(self):
        """Busca un enemigo en la posición actual. Subclases lo implementan."""
        raise NotImplementedError

    def es_atacado_por(self, alguien):
        """Recibe un ataque de alguien y pierde vidas."""
        self.vidas -= alguien.poder
        print(f"{self} es atacado por {alguien}")
        print(f"vidas: {self.vidas}")
        if self.vidas <= 0:
            self.muero()

    def esta_vivo(self):
        """Devuelve True si el ente tiene vidas restantes."""
        return self.vidas > 0

    def muero(self):
        """Comportamiento al morir. Subclases lo implementan."""
        raise NotImplementedError
