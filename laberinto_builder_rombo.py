"""
Módulo laberinto_builder_rombo.

Define la clase LaberintoBuilderRombo, variante del Builder
para laberintos con habitaciones en forma de rombo.
"""
from rombo import Rombo
from laberinto_builder import LaberintoBuilder


class LaberintoBuilderRombo(LaberintoBuilder):
    """
    LaberintoBuilderRombo es un ConcreteBuilder que construye laberintos
    con habitaciones de forma rombo (orientaciones diagonales).
    """

    def asignar_orientaciones(self, una_forma):
        """Asigna las cuatro orientaciones diagonales a una forma."""
        una_forma.agregar_orientacion(self.fabricar_noreste())
        una_forma.agregar_orientacion(self.fabricar_noroeste())
        una_forma.agregar_orientacion(self.fabricar_sureste())
        una_forma.agregar_orientacion(self.fabricar_suroeste())

    def fabricar_forma(self):
        """Crea una forma rombo con orientaciones diagonales asignadas."""
        forma = Rombo()
        self.asignar_orientaciones(forma)
        return forma
