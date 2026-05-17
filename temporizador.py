"""
Modulo temporizador.

Define la clase Temporizador, un Decorator que anade un limite de
tiempo a cualquier elemento del mapa (habitacion, bomba, bicho).
Implementa el patron Decorator igual que Bomba, Niebla y Mimico.

Variantes segun contexto:
- En habitacion: 60s para salir o mueres (pinchos)
- En bomba: 20s para desactivar
- En bicho: 20s para derrotar
- En laberinto global: 300s (5 min) o se cierran las puertas
"""
from decorator import Decorator


class Temporizador(Decorator):
    """
    Temporizador anade un limite de tiempo a un elemento del mapa.
    El tiempo se especifica en segundos.

    Implementa el patron Decorator: se agrega como hijo a cualquier
    habitacion/contenedor para modificar su comportamiento temporal.
    """

    def __init__(self, segundos=60):
        super().__init__()
        self.activa = True
        self.segundos = segundos

    def entrar(self, alguien=None):
        """Informa del temporizador y delega al elemento decorado."""
        if self.activa and alguien:
            msg = f"CUIDADO: Tienes {self.segundos}s en esta zona!"
            if hasattr(alguien, 'ultimo_evento'):
                alguien.ultimo_evento = msg
        if self.em:
            self.em.entrar(alguien)

    def es_temporizador(self):
        """Devuelve True."""
        return True

    def __str__(self):
        return f"Temporizador({self.segundos}s)"
