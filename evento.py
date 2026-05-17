"""
Módulo evento.

Define los minijuegos (eventos) que se activan al interactuar con
elementos del laberinto: Simon Dice para bombas y Piedra-Papel-Tijeras
para combate contra entes.
"""
import random
import sys
import msvcrt

# Forzar UTF-8 en la salida
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# ─── Utilidades de input ─────────────────────────────────────────────────────
def _leer_tecla_evento():
    """Lee una tecla sin necesidad de pulsar Enter (msvcrt)."""
    ch = msvcrt.getwch()
    if ch in ('\xe0', '\x00'):
        msvcrt.getwch()       # descarta segundo byte de tecla especial
        return None
    return ch.lower()


# ─── Piedra Papel Tijeras ────────────────────────────────────────────────────
class EventoPPT:
    """
    Evento Piedra-Papel-Tijeras.
    El jugador tiene 3 vidas, el ente tiene 1 vida.
    Las vidas se resetean en cada combate nuevo.
    Controles: R=Piedra, P=Papel, T=Tijeras
    """

    OPCIONES = {'r': 'PIEDRA', 'p': 'PAPEL', 't': 'TIJERAS'}
    GANA = {'r': 't', 'p': 'r', 't': 'p'}   # clave gana a valor

    def __init__(self):
        self.vidas_jugador = 3
        self.vidas_ente = 1

    def ejecutar(self, render_fn):
        """
        Ejecuta el minijuego.
        render_fn(lineas: list[str]) se usa para dibujar en pantalla.
        Devuelve True si el jugador gana, False si pierde.
        """
        self.vidas_jugador = 3
        self.vidas_ente = 1

        while self.vidas_jugador > 0 and self.vidas_ente > 0:
            v_j = "O" * self.vidas_jugador + "." * (3 - self.vidas_jugador)
            v_e = "O" * self.vidas_ente
            lineas = [
                "====== COMBATE ======",
                "",
                f"  Tus vidas:  [{v_j}]",
                f"  Ente vidas: [{v_e}]",
                "",
                "  [R] Piedra",
                "  [P] Papel",
                "  [T] Tijeras",
                "",
                "  Elige tu jugada:",
            ]
            render_fn(lineas)

            # Leer input válido
            eleccion = None
            while eleccion not in self.OPCIONES:
                eleccion = _leer_tecla_evento()

            cpu = random.choice(list(self.OPCIONES.keys()))
            nombre_j = self.OPCIONES[eleccion]
            nombre_c = self.OPCIONES[cpu]

            if eleccion == cpu:
                resultado = "EMPATE"
            elif self.GANA[eleccion] == cpu:
                resultado = "GANASTE la ronda!"
                self.vidas_ente -= 1
            else:
                resultado = "PERDISTE la ronda"
                self.vidas_jugador -= 1

            v_j = "O" * self.vidas_jugador + "." * (3 - self.vidas_jugador)
            v_e = "O" * self.vidas_ente
            lineas_res = [
                "====== COMBATE ======",
                "",
                f"  Tu: {nombre_j}  vs  Ente: {nombre_c}",
                f"  -> {resultado}",
                "",
                f"  Tus vidas:  [{v_j}]",
                f"  Ente vidas: [{v_e}]",
                "",
                "  Pulsa cualquier tecla...",
            ]
            render_fn(lineas_res)
            _leer_tecla_evento()

        ganaste = self.vidas_ente <= 0
        return ganaste


# ─── Simon Dice ──────────────────────────────────────────────────────────────
class EventoSimonDice:
    """
    Evento Simon Dice para desactivar bombas.
    Se muestra una secuencia de teclas (WASD) que el jugador debe repetir.
    Empieza con 3 teclas; si fallas, la bomba explota.
    Controles: W, A, S, D
    """

    TECLAS = ['w', 'a', 's', 'd']
    NOMBRES = {'w': '^W', 'a': '<A', 's': 'vS', 'd': '>D'}

    def __init__(self, longitud=3):
        self.longitud = longitud

    def ejecutar(self, render_fn):
        """
        Ejecuta el minijuego.
        Devuelve True si desactiva la bomba, False si explota.
        """
        secuencia = [random.choice(self.TECLAS) for _ in range(self.longitud)]
        nombres_seq = ' '.join(self.NOMBRES[t] for t in secuencia)

        # Mostrar secuencia
        lineas = [
            "====== BOMBA ======",
            "",
            "  Desactiva la bomba!",
            "  Memoriza la secuencia:",
            "",
            f"    {nombres_seq}",
            "",
            "  Pulsa cualquier tecla",
            "  cuando estes listo...",
        ]
        render_fn(lineas)
        _leer_tecla_evento()

        # Pedir repetición
        aciertos = 0
        for i, tecla_correcta in enumerate(secuencia):
            restantes = self.longitud - i
            lineas_input = [
                "====== BOMBA ======",
                "",
                f"  Paso {i + 1}/{self.longitud}",
                f"  Teclas restantes: {restantes}",
                "",
                "  Pulsa la tecla correcta",
                "  (W / A / S / D):",
            ]
            render_fn(lineas_input)

            tecla = None
            while tecla not in self.TECLAS:
                tecla = _leer_tecla_evento()

            if tecla == tecla_correcta:
                aciertos += 1
            else:
                lineas_fallo = [
                    "====== BOMBA ======",
                    "",
                    f"  INCORRECTO! Era {self.NOMBRES[tecla_correcta]}",
                    "  ** LA BOMBA HA EXPLOTADO! **",
                    "",
                    "  Pulsa cualquier tecla...",
                ]
                render_fn(lineas_fallo)
                _leer_tecla_evento()
                return False

        lineas_ok = [
            "====== BOMBA ======",
            "",
            "  BOMBA DESACTIVADA!",
            f"  {aciertos}/{self.longitud} aciertos",
            "",
            "  Pulsa cualquier tecla...",
        ]
        render_fn(lineas_ok)
        _leer_tecla_evento()
        return True
