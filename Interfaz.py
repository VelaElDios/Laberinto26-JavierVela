"""
Módulo Interfaz.

Proporciona la clase InterfazTerminal: visualización ASCII del laberinto,
captura de teclas en tiempo real mediante msvcrt (nativo Windows),
e integración de minijuegos (eventos) al interactuar con entes y bombas.
"""
# pylint: disable=invalid-name

import os
import sys
import msvcrt

from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from evento import EventoPPT, EventoSimonDice

# Forzar UTF-8 en la salida para soportar caracteres especiales
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (OSError, ValueError):
        pass

# ─── Constantes de layout ───────────────────────────────────────────────────
_W = 45          # ancho interior del recuadro (entre las ║)
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
    lpad = (_W - 9) // 2
    rpad = _W - 9 - lpad
    return f"║{' ' * lpad}{celda}{' ' * rpad}║"


def _fila_media(oeste, este, prota: str) -> str:
    """Línea del medio: [oeste] [prota] [este] — exactamente _W chars."""
    c_o = _celda(oeste)             # 9
    c_p = f"[{prota:^7}]"           # 9
    c_e = _celda(este)              # 9
    # total interior: 9+9+9 = 27, necesitamos _W = 45, así que 18 de padding
    gap = (_W - 27) // 4            # 4 (entre cada elemento y bordes)
    r = _W - 27 - gap * 4
    contenido = f"{' ' * gap}{c_o}{' ' * gap}{c_p}{' ' * gap}{c_e}{' ' * (gap + r)}"
    return f"║{contenido}║"


def _seccion(titulo: str) -> str:
    """╠══ TITULO ══╣ de ancho _W."""
    t = f" {titulo} "
    lado = (_W - len(t)) // 2
    resto = _W - len(t) - lado
    return f"╠{'═' * lado}{t}{'═' * resto}╣"


def _linea_centrada(texto: str) -> str:
    """Línea de texto centrada dentro del recuadro."""
    return f"║{texto:^{_W}}║"


# ─── Clase principal ─────────────────────────────────────────────────────────
class InterfazTerminal:
    """Interfaz de terminal para el juego del laberinto con eventos/minijuegos."""

    def __init__(self, juego):
        self.juego = juego
        self.personaje = juego.person
        self.activo = True
        self.juego.callback_fin = self._on_fin_juego

    def _on_fin_juego(self):
        """Callback que se ejecuta cuando el juego termina."""
        self.activo = False

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

        # Indicadores de contenido en la habitación
        bichos_aqui = self.juego.hay_bichos_en(pos) if pos else []
        bomba_aqui = self.juego.hay_bombas_en(pos) if pos else False

        # Construir título con info de sala
        tipo_sala = ""
        if hasattr(pos, 'es_salida') and pos.es_salida():
            tipo_sala = " [EXIT]"

        titulo = f"  LABERINTO  -  {nombre_hab}{tipo_sala}  "
        vidas_txt = f"<3 x{self.personaje.vidas}"

        # Indicadores de la sala
        indicadores = []
        if bichos_aqui:
            indicadores.append(f"[!] {len(bichos_aqui)} ente(s)")
        if bomba_aqui:
            indicadores.append("[BOMBA] Bomba activa")
        ind_txt = "  |  ".join(indicadores) if indicadores else "Sala segura"

        lineas = [
            f"╔{_SEP}╗",
            f"║{titulo:^{_W}}║",
            _seccion(f"VIDAS: {vidas_txt}"),
            _linea_centrada(ind_txt),
            _seccion("MAPA"),
            f"║{' ' * _W}║",
            _fila_cara(norte),
            f"║{' ' * _W}║",
            _fila_media(oeste, este, prota),
            f"║{' ' * _W}║",
            _fila_cara(sur),
            f"║{' ' * _W}║",
            _seccion("EVENTO"),
            _linea_centrada(evento[:_W - 2] if len(evento) > _W - 2 else evento),
            _seccion("CONTROLES"),
            _linea_centrada("W/↑ Norte    S/↓ Sur"),
            _linea_centrada("A/← Oeste    D/→ Este"),
            _linea_centrada("Q: Salir"),
            f"╚{_SEP}╝",
        ]
        print("\n".join(lineas))

    def _render_evento(self, lineas_evento):
        """Renderiza un minijuego dentro del marco del interfaz."""
        os.system('cls')
        lineas = [f"╔{_SEP}╗"]
        for linea in lineas_evento:
            if len(linea) > _W - 2:
                linea = linea[:_W - 2]
            lineas.append(_linea_centrada(linea))
        lineas.append(f"╚{_SEP}╝")
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
            self.personaje.ir_a(or_)

    # ── Eventos / Minijuegos ─────────────────────────────────────────────────
    def _comprobar_eventos(self):
        """
        Comprueba si en la posición actual hay eventos que activar:
        - Bichos → Piedra Papel Tijeras
        - Bombas → Simón Dice
        """
        if self.juego.finalizado:
            return

        pos = self.personaje.posicion
        if not pos:
            return

        # ¿Hay bichos?
        bichos = self.juego.hay_bichos_en(pos)
        for bicho in bichos:
            self.personaje.ultimo_evento = f"Un {bicho} te ataca! Piedra-Papel-Tijeras"
            self._render()
            msvcrt.getwch()  # espera una tecla para empezar

            evento = EventoPPT()
            ganaste = evento.ejecutar(self._render_evento)

            if ganaste:
                self.personaje.ultimo_evento = f"Has derrotado a {bicho}!"
                self.juego.muere_bicho(bicho)
            else:
                self.personaje.vidas -= 1
                self.personaje.ultimo_evento = (
                    f"¡{bicho} te ha derrotado! Pierdes 1 vida "
                    f"(quedan {self.personaje.vidas})"
                )
                if self.personaje.vidas <= 0:
                    self.juego.muere_personaje()
                    return

            if self.juego.finalizado:
                return

        # ¿Hay bombas?
        if self.juego.hay_bombas_en(pos):
            self.personaje.ultimo_evento = "BOMBA! Desactivala con Simon Dice"
            self._render()
            msvcrt.getwch()

            evento = EventoSimonDice(longitud=3)
            desactivada = evento.ejecutar(self._render_evento)

            if desactivada:
                self.personaje.ultimo_evento = "Bomba desactivada!"
                # Desactivar las bombas en la habitación
                for hijo in list(getattr(pos, 'hijos', [])):
                    if getattr(hijo, 'es_bomba', lambda: False)():
                        hijo.activa = False
            else:
                self.personaje.vidas -= 1
                self.personaje.ultimo_evento = (
                    f"La bomba exploto! Pierdes 1 vida "
                    f"(quedan {self.personaje.vidas})"
                )
                if self.personaje.vidas <= 0:
                    self.juego.muere_personaje()
                    return

    # ── Pantallas finales ─────────────────────────────────────────────────────
    def _pantalla_victoria(self):
        """Muestra la pantalla de victoria."""
        os.system('cls')
        lineas = [
            f"╔{_SEP}╗",
            _linea_centrada(""),
            _seccion("*** VICTORIA ***"),
            _linea_centrada(""),
            _linea_centrada(f"{self.personaje.nombre} ha escapado del laberinto!"),
            _linea_centrada(""),
            _linea_centrada(f"Vidas restantes: <3 x{self.personaje.vidas}"),
            _linea_centrada(f"Entes derrotados: {self._entes_derrotados()}"),
            _linea_centrada(""),
            _linea_centrada("Enhorabuena!"),
            _linea_centrada(""),
            _linea_centrada("Pulsa cualquier tecla para salir..."),
            _linea_centrada(""),
            f"╚{_SEP}╝",
        ]
        print("\n".join(lineas))
        msvcrt.getwch()

    def _pantalla_derrota(self):
        """Muestra la pantalla de derrota."""
        os.system('cls')
        lineas = [
            f"╔{_SEP}╗",
            _linea_centrada(""),
            _seccion("*** GAME OVER ***"),
            _linea_centrada(""),
            _linea_centrada(f"{self.personaje.nombre} no ha sobrevivido..."),
            _linea_centrada(""),
            _linea_centrada("¡Mejor suerte la próxima vez!"),
            _linea_centrada(""),
            _linea_centrada("Pulsa cualquier tecla para salir..."),
            _linea_centrada(""),
            f"╚{_SEP}╝",
        ]
        print("\n".join(lineas))
        msvcrt.getwch()

    def _entes_derrotados(self):
        """Cuenta los bichos que ya no están vivos."""
        return sum(1 for b in self.juego.bichos if not b.esta_vivo())

    # ── Bucle principal ───────────────────────────────────────────────────────
    def bucle_principal(self):
        """Lanza el bucle de juego interactivo. Bloquea hasta que el jugador salga."""
        self.personaje.ultimo_evento = "¡Bienvenido! Usa WASD o flechas. Llega a la SALIDA."
        self._render()

        while self.activo and not self.juego.finalizado:
            accion = self._leer_tecla()
            if accion == 'salir':
                self.activo = False
            elif accion:
                self.personaje.ultimo_evento = ""
                self._mover(accion)

                # Comprobar eventos en la nueva posición
                if not self.juego.finalizado:
                    self._comprobar_eventos()

                self._render()

        # Pantalla final
        if self.juego.finalizado:
            if self.juego.resultado == "victoria":
                self._pantalla_victoria()
            elif self.juego.resultado == "derrota":
                self._pantalla_derrota()
        else:
            os.system('cls')
            print("¡Hasta pronto!")
