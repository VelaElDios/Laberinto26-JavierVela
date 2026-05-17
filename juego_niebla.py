"""
Módulo juego_niebla.

Define la clase JuegoNiebla, subclase de Juego que coloca niebla
en todas las habitaciones usando el patron Factory Method.
"""
from juego import Juego
from niebla import Niebla


class JuegoNiebla(Juego):
    """
    JuegoNiebla ilustra el patron Factory Method:
    tras fabricar cada habitacion, le anade una Niebla como hijo.
    Equivalente a JuegoBombas pero con niebla.
    """

    def fabricar_habitacion_num(self, un_num):
        """Crea una habitacion con niebla usando Factory Method."""
        hab = super().fabricar_habitacion_num(un_num)
        niebla = Niebla()
        niebla.activa = True
        hab.agregar_hijo(niebla)
        return hab
