"""
Módulo puerta.

Define la clase Puerta, elemento que comunica dos habitaciones.
"""
from hoja import Hoja


class Puerta(Hoja):
    """
    Puerta es un elemento del mapa que une dos habitaciones.
    Puede estar abierta o cerrada.
    """

    def __init__(self):
        super().__init__()
        self.abierta = False
        self.lado1 = None
        self.lado2 = None

    def abrir(self):
        """Abre la puerta."""
        print(f"Abrimos {self}")
        self.abierta = True

    def cerrar(self):
        """Cierra la puerta."""
        print(f"Cerramos {self}")
        self.abierta = False

    def entrar(self, alguien):
        """Permite o bloquea el paso según si la puerta está abierta."""
        if self.abierta:
            if getattr(alguien, 'posicion', None) == self.lado1:
                if self.lado2:
                    self.lado2.entrar(alguien)
            else:
                if self.lado1:
                    self.lado1.entrar(alguien)
        else:
            msg = "La puerta está cerrada."
            if hasattr(alguien, 'ultimo_evento'):
                alguien.ultimo_evento = msg
            else:
                print(msg)

    def es_puerta(self):
        """Devuelve True."""
        return True

    def __str__(self):
        return f"Puerta-{getattr(self.lado1, 'num', 'None')}-{getattr(self.lado2, 'num', 'None')}"
