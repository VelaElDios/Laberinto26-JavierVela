"""
Módulo forma.

Define la clase base Forma, implementación del patrón Bridge
que desacopla la abstracción (Contenedor) de la forma geométrica.
"""
import random


class Forma:
    """
    Forma es la implementación de la abstracción (contenedores)
    según el patrón Bridge.
    """

    def __init__(self):
        self.orientaciones = []
        self.num = None

    def agregar_orientacion(self, una_or):
        """Añade una orientación a esta forma."""
        self.orientaciones.append(una_or)

    def eliminar_orientacion(self, una_or):
        """Elimina una orientación de esta forma."""
        if una_or in self.orientaciones:
            self.orientaciones.remove(una_or)

    def obtener_orientacion_aleatoria(self):
        """Devuelve una orientación aleatoria de las disponibles."""
        if not self.orientaciones:
            return None
        return random.choice(self.orientaciones)

    def poner_en_elemento(self, una_or, un_em):
        """Coloca un_em en el lado indicado por una_or."""
        una_or.poner_elemento_en_contenedor(un_em, self)
