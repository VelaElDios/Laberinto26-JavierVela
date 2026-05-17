"""
Módulo elemento_mapa.

Define la clase base ElementoMapa, interfaz común de todos los
elementos del laberinto.
"""


class ElementoMapa:
    """
    ElementoMapa es la interfaz común de los elementos del laberinto.
    """

    def entrar(self, alguien):
        """Define el comportamiento al entrar en este elemento."""
        raise NotImplementedError

    def es_bomba(self):
        """Devuelve True si el elemento es una bomba."""
        return False

    def es_puerta(self):
        """Devuelve True si el elemento es una puerta."""
        return False

    def es_salida(self):
        """Devuelve True si el elemento es una habitación de salida."""
        return False

    def es_niebla(self):
        """Devuelve True si el elemento tiene niebla."""
        return False

    def es_mimico(self):
        """Devuelve True si el elemento es mimico."""
        return False

    def es_tienda(self):
        """Devuelve True si el elemento es una tienda."""
        return False

    def es_temporizador(self):
        """Devuelve True si el elemento es un temporizador."""
        return False

    def recorrer(self, un_bloque):
        """Recorre el elemento aplicando un_bloque."""
        raise NotImplementedError
