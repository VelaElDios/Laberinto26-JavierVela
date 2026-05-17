"""
Módulo niebla.

Define la clase Niebla, un Decorator que oculta la visibilidad
de las salidas de una habitacion. Implementa el patron Decorator
igual que Bomba.
"""
from decorator import Decorator


class Niebla(Decorator):
    """
    Niebla es un elemento del mapa que oculta la visibilidad
    de las salidas cuando el personaje esta dentro.
    Implementa el patron Decorator anadiendo comportamiento de ocultacion.

    En una habitacion con niebla:
    - No se ven las salidas (puertas/paredes) en la interfaz
    - Las bombas tienen secuencia de 4 en vez de 3
    - Contra entes se tienen 2 vidas en vez de 3
    """

    def __init__(self):
        super().__init__()
        self.activa = True

    def entrar(self, alguien=None):
        """Informa de la niebla y delega al elemento decorado."""
        if self.activa:
            msg = "Has entrado en una zona de NIEBLA... no ves nada."
            if alguien and hasattr(alguien, 'ultimo_evento'):
                alguien.ultimo_evento = msg
            else:
                if alguien:
                    print(f"{alguien} entra en niebla")
        if self.em:
            self.em.entrar(alguien)

    def es_niebla(self):
        """Devuelve True."""
        return True

    def __str__(self):
        return "Niebla"
