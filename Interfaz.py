"""
Módulo Interfaz.

Proporciona la clase InterfazTerminal: visualización ASCII del laberinto
y captura de teclas en tiempo real mediante msvcrt (nativo Windows).
"""
# pylint: disable=invalid-name

import os
import msvcrt

from Orientaciones import Norte, Sur, Este, Oeste

# ─── Constantes de layout ───────────────────────────────────────────────────
_W = 33          # ancho interior del recuadro (entre las ║)
_SEP = '═' * _W  # separador horizontal completo


# ─── Símbolos de elementos ──────────────────────────────────────────────────
def _sym(elem) -> str:
    """Devuelve una cadena de exactamente 7 chars para representar un elemento."""
    if elem is None:
        return "  ...  "
    nombre = type(elem).__name__
    if nombre == 'ParedBomba':
        return " BOMBA "
    if nombre == 'Pared':
        return "███████"
    if nombre == 'Puerta':
        return " OPEN  " if elem.abierta else " DOOR  "
    return f" {nombre[:5]:^5} "


def _celda(elem) -> str:
    """Envuelve el símbolo en corchetes: 9 chars en total."""
    return f"[{_sym(elem)}]"


def _fila_cara(elem) -> str:
    """Línea de norte o sur: celda centrada en _W."""
    celda = _celda(elem)             # 9 chars
    lpad = (_W - 9) // 2            # 12
    rpad = _W - 9 - lpad            # 12
    return f"║{' ' * lpad}{celda}{' ' * rpad}║"


def _fila_media(oeste, este, prota: str) -> str:
    """Línea del medio: [oeste] [prota] [este] — exactamente _W=33 chars."""
    c_o = _celda(oeste)             # 9
    c_p = f"[{prota:^7}]"           # 9
    c_e = _celda(este)              # 9
    # 1 + 9 + 2 + 9 + 2 + 9 + 1 = 33 ✓
    contenido = f" {c_o}  {c_p}  {c_e} "
    return f"║{contenido}║"


def _seccion(titulo: str) -> str:
    """╠══ TITULO ══╣ de ancho _W."""
    t = f" {titulo} "
    lado = (_W - len(t)) // 2
    resto = _W - len(t) - lado
    return f"╠{'═' * lado}{t}{'═' * resto}╣"


# ─── Clase principal ─────────────────────────────────────────────────────────
class InterfazTerminal:
    """Interfaz de terminal para el juego del laberinto."""

    def __init__(self, juego):
        self.juego = juego
        self.personaje = juego.person
        self.activo = True

    # ── Render ────────────────────────────────────────────────────────────────
    def _render(self):
        """Limpia la pantalla y dibuja el estado actual del juego."""
        os.system('cls')

        pos = self.personaje.posicion
        nombre_hab = str(pos) if pos else "???"
        forma = getattr(pos, 'forma', None)

        norte = getattr(forma, 'norte', None)
        sur   = getattr(forma, 'sur',   None)
        este  = getattr(forma, 'este',  None)
        oeste = getattr(forma, 'oeste', None)

        prota = (self.personaje.nombre or "Héroe")[:5]
        evento = self.personaje.ultimo_evento or " "

        titulo = f"  LABERINTO  —  {nombre_hab}  "

        lineas = [
            f"╔{_SEP}╗",
            f"║{titulo:^{_W}}║",
            _seccion("MAPA"),
            f"║{' ' * _W}║",
            _fila_cara(norte),
            f"║{' ' * _W}║",
            _fila_media(oeste, este, prota),
            f"║{' ' * _W}║",
            _fila_cara(sur),
            f"║{' ' * _W}║",
            _seccion("EVENTO"),
            f"║{evento:^{_W}}║",
            _seccion("CONTROLES"),
            f"║{'  W / ↑  Norte       S / ↓  Sur':^{_W}}║",
            f"║{'  A / ←  Oeste       D / →  Este':^{_W}}║",
            f"║{'Q : Salir':^{_W}}║",
            f"╚{_SEP}╝",
        ]
        print("\n".join(lineas))

    # ── Input ─────────────────────────────────────────────────────────────────
    def _leer_tecla(self):
        """Captura una tecla sin necesidad de pulsar Enter (msvcrt)."""
        ch = msvcrt.getwch()
        if ch in ('\xe0', '\x00'):          # tecla especial: flechas, F-keys…
            ch2 = msvcrt.getwch()
            return {
                'H': 'norte',   # flecha ↑
                'P': 'sur',     # flecha ↓
                'K': 'oeste',   # flecha ←
                'M': 'este',    # flecha →
            }.get(ch2)
        return {
            'w': 'norte', 'W': 'norte',
            's': 'sur',   'S': 'sur',
            'a': 'oeste', 'A': 'oeste',
            'd': 'este',  'D': 'este',
            'q': 'salir', 'Q': 'salir',
        }.get(ch)

    # ── Movimiento ────────────────────────────────────────────────────────────
    def _mover(self, direccion: str):
        """Traduce la dirección a orientación y mueve al personaje."""
        mapa_orientaciones = {
            'norte': Norte.default(),
            'sur':   Sur.default(),
            'este':  Este.default(),
            'oeste': Oeste.default(),
        }
        or_ = mapa_orientaciones.get(direccion)
        if or_:
            try:
                self.personaje.ir_a(or_)
            except AttributeError:
                self.personaje.ultimo_evento = "No puedes ir en esa dirección."

    # ── Bucle principal ───────────────────────────────────────────────────────
    def bucle_principal(self):
        """Lanza el bucle de juego interactivo. Bloquea hasta que el jugador salga."""
        self.personaje.ultimo_evento = "¡Bienvenido! Usa WASD o las flechas para moverte."
        self._render()

        while self.activo:
            accion = self._leer_tecla()
            if accion == 'salir':
                self.activo = False
            elif accion:
                self.personaje.ultimo_evento = ""
                self._mover(accion)
                self._render()

        os.system('cls')
        print("¡Hasta pronto!")
