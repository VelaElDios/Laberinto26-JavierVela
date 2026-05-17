"""
Modulo mimico.

Define la clase Mimico, un Decorator que invierte las reglas
de los eventos del laberinto. Aplica tanto a bombas como a entes.
En combate PPT: las reglas se invierten.
En Simon Dice: los controles se invierten.
"""
from decorator import Decorator


class Mimico(Decorator):
    """
    Mimico es un elemento del mapa que invierte las reglas de los
    minijuegos cuando el personaje interactua con entes o bombas.

    Implementa el patron Decorator igual que Bomba y Niebla.

    Efectos:
    - PPT: Tijera gana a Piedra, Piedra gana a Papel, Papel gana a Tijera
    - Simon Dice: Arriba=Abajo, Derecha=Izquierda
    """

    def __init__(self):
        super().__init__()
        self.activa = True

    def entrar(self, alguien=None):
        """Informa del mimico y delega al elemento decorado."""
        if self.activa:
            msg = "Algo se siente... RARO en esta sala."
            if alguien and hasattr(alguien, 'ultimo_evento'):
                alguien.ultimo_evento = msg
            else:
                if alguien:
                    print(f"{alguien} detecta algo raro")
        if self.em:
            self.em.entrar(alguien)

    def es_mimico(self):
        """Devuelve True."""
        return True

    def __str__(self):
        return "Mimico"
