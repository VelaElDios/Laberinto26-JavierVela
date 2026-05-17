"""
Modulo juego_tiempo.

Define la clase JuegoTiempo, subclase de Juego que coloca
temporizadores en todas las habitaciones usando Factory Method.
Equivalente a JuegoBombas/JuegoNiebla pero con temporizadores.
"""
from juego import Juego
from temporizador import Temporizador


class JuegoTiempo(Juego):
    """
    JuegoTiempo (Laberinto del Tiempo) ilustra el patron Factory Method:
    tras fabricar cada habitacion, le anade un Temporizador como hijo.
    Todas las habitaciones tendran limite de tiempo.
    """

    def fabricar_habitacion_num(self, un_num):
        """Crea una habitacion con temporizador usando Factory Method."""
        hab = super().fabricar_habitacion_num(un_num)
        temp = Temporizador(segundos=60)
        temp.activa = True
        hab.agregar_hijo(temp)
        return hab
