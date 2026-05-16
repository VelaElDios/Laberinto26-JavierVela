"""
Módulo contenedor.

Define la clase Contenedor, elemento compuesto del laberinto.
Corresponde al rol Composite del patrón Composite.
"""
from elemento_mapa import ElementoMapa


class Contenedor(ElementoMapa):
    """
    Contenedor es un elemento del mapa que tiene hijos.
    Es el Composite del patrón Composite.
    """

    def __init__(self):
        self.hijos = []
        self.forma = None
        self.num = None

    def agregar_hijo(self, un_em):
        """Añade un elemento hijo a este contenedor."""
        self.hijos.append(un_em)

    def agregar_orientacion(self, una_or):
        """Delega la orientación a la forma del contenedor."""
        if self.forma:
            self.forma.agregar_orientacion(una_or)

    def eliminar_hijo(self, un_em):
        """Elimina un elemento hijo de este contenedor."""
        if un_em in self.hijos:
            self.hijos.remove(un_em)

    def eliminar_orientacion(self, una_or):
        """Elimina una orientación de la forma del contenedor."""
        if self.forma:
            self.forma.eliminar_orientacion(una_or)

    def entrar(self, alguien):
        """Hace entrar a alguien en este contenedor."""
        alguien.posicion = self
        msg = f"Estás en {self}."
        if hasattr(alguien, 'ultimo_evento'):
            alguien.ultimo_evento = msg
        else:
            print(f"{alguien} está en {self}")

    def ir_al_norte(self, alguien):
        """Mueve a alguien hacia el norte dentro de la forma."""
        if self.forma:
            self.forma.ir_al_norte(alguien)

    def obtener_orientacion_aleatoria(self):
        """Devuelve una orientación aleatoria de la forma."""
        if self.forma:
            return self.forma.obtener_orientacion_aleatoria()
        return None

    def poner_en_elemento(self, una_or, un_em):
        """Coloca un elemento en la dirección indicada por la orientación."""
        if self.forma:
            self.forma.poner_en_elemento(una_or, un_em)

    def recorrer(self, un_bloque):
        """Recorre el contenedor y todos sus hijos aplicando un_bloque."""
        print(str(self))
        un_bloque(self)
        for hijo in self.hijos:
            hijo.recorrer(un_bloque)

        if self.forma and hasattr(self.forma, 'orientaciones'):
            for orien in self.forma.orientaciones:
                orien.recorrer_en_contenedor(un_bloque, self.forma)
