"""
Módulo hoja.

Define la clase Hoja, elemento simple (sin hijos) del laberinto.
Corresponde al rol Leaf del patrón Composite.
"""
from elemento_mapa import ElementoMapa


class Hoja(ElementoMapa):
    """
    Hoja es la interfaz de los elementos simples del laberinto.
    Es el Leaf del patrón Composite.
    """

    def entrar(self, alguien):
        """Comportamiento por defecto al intentar entrar en una hoja."""
        raise NotImplementedError

    def recorrer(self, un_bloque):
        """Recorre la hoja aplicando un_bloque sobre ella misma."""
        print(str(self))
        un_bloque(self)
