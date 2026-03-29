import random

class Forma:
    """
    Forma es la implementación de la abstracción (contenedores), según el patrón Bridge.
    """
    def __init__(self):
        self.orientaciones = []
        self.num = None

    def agregar_orientacion(self, una_or):
        self.orientaciones.append(una_or)

    def eliminar_orientacion(self, una_or):
        if una_or in self.orientaciones:
            self.orientaciones.remove(una_or)

    def obtener_orientacion_aleatoria(self):
        if not self.orientaciones:
            return None
        return random.choice(self.orientaciones)

    def poner_en_elemento(self, una_or, un_em):
        una_or.poner_elemento_en_contenedor(un_em, self)


class Cuadrado(Forma):
    """
    Es un polígono regular de 4 lados.
    """
    def __init__(self):
        super().__init__()
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None


class Rombo(Forma):
    """
    Rombo es un polígono con orientaciones ne no se so
    """
    def __init__(self):
        super().__init__()
        self.ne = None
        self.no = None
        self.se = None
        self.so = None
