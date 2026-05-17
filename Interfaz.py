"""
Módulo Interfaz.

Proporciona la clase InterfazTerminal: visualización ASCII del laberinto,
captura de teclas en tiempo real mediante msvcrt (nativo Windows),
e integración de minijuegos (eventos) al interactuar con entes y bombas.
"""
# pylint: disable=invalid-name

import os
import sys
import time
import ctypes
import msvcrt

from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from evento import EventoPPT, EventoSimonDice, EventoTienda

# Forzar UTF-8 en la salida para soportar caracteres especiales
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (OSError, ValueError):
        pass

# Habilitar secuencias ANSI en Windows (evita parpadeo)
try:
    _kernel32 = ctypes.windll.kernel32
    _kernel32.SetConsoleMode(_kernel32.GetStdHandle(-11), 7)
except (AttributeError, OSError):
    pass


def _home_cursor():
    """Mueve el cursor al inicio sin borrar — evita parpadeo."""
    print('\033[H', end='', flush=True)


def _clear_below():
    """Borra desde el cursor hasta el final de la pantalla."""
    print('\033[0J', end='', flush=True)

# ─── Constantes de layout ───────────────────────────────────────────────────
_W = 60          # ancho interior del recuadro (entre las ║)
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

    # Multiplicadores de tiempo por clase
    MULT_TIEMPO = {
        'alumno':   1.5,   # mas tiempo
        'guerrero': 0.75,  # menos tiempo
        'profesor': 1.0,   # normal
    }

    def __init__(self, juego):
        self.juego = juego
        self.personaje = juego.person
        self.activo = True
        self.juego.callback_fin = self._on_fin_juego
        # Temporizadores
        self.tiempo_entrada_sala = time.time()
        self.sala_anterior = None
        self.tiempo_inicio_global = time.time()

    def _on_fin_juego(self):
        """Callback que se ejecuta cuando el juego termina."""
        self.activo = False

    def _mult(self):
        """Devuelve el multiplicador de tiempo segun la clase."""
        return self.MULT_TIEMPO.get(self.personaje.clase, 1.0)

    # ── Menu principal ────────────────────────────────────────────────────────
    def _menu_principal(self):
        """Muestra el menu principal y configura dificultad/clase."""
        dificultad = "normal"
        clase = "alumno"

        while True:
            os.system('cls')
            dif_disp = dificultad.upper()
            cls_disp = clase.upper()
            lineas = [
                f"╔{_SEP}╗",
                _linea_centrada(""),
                _seccion("LABERINTO 26"),
                _linea_centrada(""),
                _linea_centrada("Un juego de Javier Vela"),
                _linea_centrada(""),
                _seccion("CONFIGURACION"),
                _linea_centrada(f"Dificultad: {dif_disp}"),
                _linea_centrada(f"Clase:      {cls_disp}"),
                _linea_centrada(""),
                _seccion("MENU"),
                _linea_centrada("[1] Jugar"),
                _linea_centrada("[2] Dificultad"),
                _linea_centrada("[3] Clase"),
                _linea_centrada("[4] Salir"),
                _linea_centrada(""),
                f"╚{_SEP}╝",
            ]
            print("\n".join(lineas))

            tecla = None
            while tecla not in ('1', '2', '3', '4'):
                tecla = msvcrt.getwch()

            if tecla == '1':
                # Aplicar configuracion
                self.personaje.dificultad = dificultad
                self.personaje.clase = clase
                if dificultad == "dificil":
                    self.personaje.vidas = 2
                else:
                    self.personaje.vidas = 3
                return True  # jugar

            elif tecla == '2':
                dificultad = self._submenu_dificultad(dificultad)

            elif tecla == '3':
                clase = self._submenu_clase(clase)

            elif tecla == '4':
                return False  # salir

    def _submenu_dificultad(self, actual):
        """Submenu para elegir dificultad."""
        os.system('cls')
        lineas = [
            f"╔{_SEP}╗",
            _linea_centrada(""),
            _seccion("DIFICULTAD"),
            _linea_centrada(""),
            _linea_centrada("[1] Normal  (3 vidas)"),
            _linea_centrada("[2] Dificil (2 vidas)"),
            _linea_centrada(""),
            _linea_centrada(f"Actual: {actual.upper()}"),
            _linea_centrada(""),
            f"╚{_SEP}╝",
        ]
        print("\n".join(lineas))
        tecla = None
        while tecla not in ('1', '2'):
            tecla = msvcrt.getwch()
        return "normal" if tecla == '1' else "dificil"

    def _submenu_clase(self, actual):
        """Submenu para elegir clase."""
        os.system('cls')
        lineas = [
            f"╔{_SEP}╗",
            _linea_centrada(""),
            _seccion("CLASE"),
            _linea_centrada(""),
            _linea_centrada("[1] Alumno"),
            _linea_centrada("    +50% tiempo en temporizadores"),
            _linea_centrada(""),
            _linea_centrada("[2] Guerrero"),
            _linea_centrada("    Puede comprar Espada (auto-win combate)"),
            _linea_centrada("    -25% tiempo en temporizadores"),
            _linea_centrada(""),
            _linea_centrada("[3] Profesor"),
            _linea_centrada("    Las bombas se desactivan solas"),
            _linea_centrada(""),
            _linea_centrada(f"Actual: {actual.upper()}"),
            _linea_centrada(""),
            f"╚{_SEP}╝",
        ]
        print("\n".join(lineas))
        tecla = None
        while tecla not in ('1', '2', '3'):
            tecla = msvcrt.getwch()
        return {
            '1': 'alumno',
            '2': 'guerrero',
            '3': 'profesor',
        }[tecla]

    # ── Render ────────────────────────────────────────────────────────────────
    def _render(self):
        """Limpia la pantalla y dibuja el estado actual del juego."""
        _home_cursor()

        pos = self.personaje.posicion
        nombre_hab = str(pos) if pos else "???"
        forma = getattr(pos, 'forma', None)

        # Detectar niebla
        niebla = self.juego.hay_niebla_en(pos) if pos else False

        # En niebla no se ven las salidas
        if niebla:
            norte = None
            sur = None
            este = None
            oeste = None
        else:
            norte = getattr(forma, 'norte', None)
            sur   = getattr(forma, 'sur',   None)
            este  = getattr(forma, 'este',  None)
            oeste = getattr(forma, 'oeste', None)

        prota = (self.personaje.nombre or "Heroe")[:5]
        evento = self.personaje.ultimo_evento or " "

        # Indicadores de contenido en la habitacion
        bichos_aqui = self.juego.hay_bichos_en(pos) if pos else []
        bomba_aqui = self.juego.hay_bombas_en(pos) if pos else False
        mimico = self.juego.hay_mimico_en(pos) if pos else False
        es_tienda = self.juego.es_tienda_en(pos) if pos else False
        tiene_timer = self.juego.hay_temporizador_en(pos) if pos else False

        # Construir titulo con info de sala
        tipo_sala = ""
        if hasattr(pos, 'es_salida') and pos.es_salida():
            tipo_sala = " [EXIT]"
        elif es_tienda:
            tipo_sala = " [TIENDA]"

        titulo = f"  LABERINTO  -  {nombre_hab}{tipo_sala}  "
        # Stats lines
        vidas_txt = f"<3 x{self.personaje.vidas}"
        sangre_txt = f"Sangre:{self.personaje.sangre}"
        clase_txt = self.personaje.clase.upper()
        dif_txt_s = self.personaje.dificultad.upper()
        equip = []
        if self.personaje.tiene_espada:
            equip.append("ESPADA")
        equip_txt = " | ".join(equip) if equip else "-"

        # Indicadores de la sala
        indicadores = []
        if niebla:
            indicadores.append("[NIEBLA]")
        if mimico:
            indicadores.append("[MIMICO]")
        if bichos_aqui:
            indicadores.append(f"[!] {len(bichos_aqui)} ente(s)")
        if bomba_aqui:
            indicadores.append("[BOMBA]")
        if es_tienda:
            indicadores.append("[TIENDA]")
        if tiene_timer:
            seg_sala = self.juego.obtener_tiempo_habitacion(pos)
            seg_real = seg_sala * self._mult()
            elapsed = time.time() - self.tiempo_entrada_sala
            rest_sala = max(0, int(seg_real - elapsed))
            indicadores.append(f"[TIMER:{rest_sala}s]")
        # Timer global
        timer_global_txt = ""
        if self.juego.timer_global:
            tg_real = self.juego.timer_global * self._mult()
            elapsed_g = time.time() - self.tiempo_inicio_global
            rest_g = max(0, int(tg_real - elapsed_g))
            timer_global_txt = f"  Global:{rest_g}s"
        ind_txt = " | ".join(indicadores) if indicadores else "Sala segura"

        # Simbolo especial para niebla
        niebla_sym = "[ ??? ]" if niebla else None

        # Separar evento en lineas si es largo
        ev_linea1 = evento[:_W - 2] if len(evento) > _W - 2 else evento
        ev_linea2 = evento[_W - 2: (_W - 2) * 2] if len(evento) > _W - 2 else ""

        lineas = [
            f"╔{_SEP}╗",
            f"║{titulo:^{_W}}║",
            _seccion(f"{vidas_txt}  {sangre_txt}{timer_global_txt}"),
            _linea_centrada(
                f"Clase: {clase_txt}  Dif: {dif_txt_s}  Equip: {equip_txt}"
            ),
            _linea_centrada(ind_txt),
            _seccion("NIEBLA" if niebla else "MAPA"),
            f"║{' ' * _W}║",
            _fila_cara(norte) if not niebla else _linea_centrada("[ ??? ]"),
            f"║{' ' * _W}║",
            _fila_media(oeste, este, prota) if not niebla else _linea_centrada(f"[ ??? ]  [{prota:^5}]  [ ??? ]"),
            f"║{' ' * _W}║",
            _fila_cara(sur) if not niebla else _linea_centrada("[ ??? ]"),
            f"║{' ' * _W}║",
            _seccion("EVENTO"),
            _linea_centrada(ev_linea1),
            _linea_centrada(ev_linea2),
            _seccion("CONTROLES"),
            _linea_centrada("W/^ Norte    S/v Sur"),
            _linea_centrada("A/< Oeste    D/> Este"),
            _linea_centrada("Q: Salir"),
            f"╚{_SEP}╝",
        ]
        print("\n".join(lineas))
        _clear_below()

    def _render_evento(self, lineas_evento):
        """Renderiza un minijuego dentro del marco del interfaz."""
        _home_cursor()
        lineas = [f"╔{_SEP}╗"]
        for linea in lineas_evento:
            if len(linea) > _W - 2:
                linea = linea[:_W - 2]
            lineas.append(_linea_centrada(linea))
        lineas.append(f"╚{_SEP}╝")
        print("\n".join(lineas))
        _clear_below()

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
        Comprueba si en la posicion actual hay eventos que activar:
        - Entes agresivos -> Piedra Papel Tijeras
        - Entes perezosos -> Tienda (venden vida por sangre)
        - Bombas -> Simon Dice
        - Habitacion tienda -> Tienda del vendedor
        Niebla y mimico modifican la dificultad/reglas.
        """
        if self.juego.finalizado:
            return

        pos = self.personaje.posicion
        if not pos:
            return

        # Detectar modificadores de sala
        niebla = self.juego.hay_niebla_en(pos)
        mimico = self.juego.hay_mimico_en(pos)
        tiene_timer = self.juego.hay_temporizador_en(pos)
        tiempo_sala = self.juego.obtener_tiempo_habitacion(pos) if tiene_timer else None
        dif_mods = []
        if niebla:
            dif_mods.append("NIEBLA")
        if mimico:
            dif_mods.append("MIMICO")
        if tiene_timer:
            dif_mods.append("TIMER")
        dif_txt = f" [{'+'.join(dif_mods)}]" if dif_mods else ""

        # Timer para eventos = 20s * mult si hay temporizador en sala
        tiempo_evento = None
        if tiene_timer:
            tiempo_evento = int(20 * self._mult())

        # ¿Hay bichos?
        bichos = self.juego.hay_bichos_en(pos)
        for bicho in bichos:
            # Comprobar si es perezoso -> tienda ambulante
            es_perezoso = hasattr(bicho, 'modo') and (
                type(bicho.modo).__name__ == 'Perezoso'
            )

            if es_perezoso:
                # Perezoso = tienda ambulante
                self.personaje.ultimo_evento = (
                    f"{bicho} quiere comerciar contigo!"
                )
                self._render()
                msvcrt.getwch()
                tienda = EventoTienda(
                    precio=2,
                    nombre_vendedor=str(bicho)
                )
                tienda.ejecutar(
                    self._render_evento, self.personaje
                )
                self.personaje.ultimo_evento = "Fin del comercio."
            else:
                # Guerrero con espada -> auto-win
                if (self.personaje.clase == 'guerrero'
                        and self.personaje.tiene_espada):
                    self.personaje.sangre += 1
                    self.personaje.ultimo_evento = (
                        f"Tu espada derrota a {bicho}! "
                        f"+1 sangre (total: {self.personaje.sangre})"
                    )
                    self.juego.muere_bicho(bicho)
                    self._render()
                    time.sleep(1)
                    continue

                # Agresivo = combate PPT
                self.personaje.ultimo_evento = (
                    f"Un {bicho} te ataca!{dif_txt} "
                    "Piedra-Papel-Tijeras"
                )
                self._render()
                msvcrt.getwch()

                evento = EventoPPT(
                    mimico=mimico,
                    tiempo_limite=tiempo_evento
                )
                # En niebla: 2 vidas (o 1 en dificil)
                if niebla:
                    if self.personaje.dificultad == "dificil":
                        evento.vidas_jugador = 1
                    else:
                        evento.vidas_jugador = 2
                elif self.personaje.dificultad == "dificil":
                    evento.vidas_jugador = 2

                ganaste = evento.ejecutar(self._render_evento)

                if ganaste:
                    # Dar sangre por la kill
                    self.personaje.sangre += 1
                    self.personaje.ultimo_evento = (
                        f"Has derrotado a {bicho}! "
                        f"+1 sangre (total: {self.personaje.sangre})"
                    )
                    self.juego.muere_bicho(bicho)
                else:
                    self.personaje.vidas -= 1
                    self.personaje.ultimo_evento = (
                        f"{bicho} te ha derrotado! Pierdes 1 vida "
                        f"(quedan {self.personaje.vidas})"
                    )
                    if self.personaje.vidas <= 0:
                        self.juego.muere_personaje()
                        return

            if self.juego.finalizado:
                return

        # ¿Hay bombas?
        if self.juego.hay_bombas_en(pos):
            # Profesor -> auto-desactiva
            if self.personaje.clase == 'profesor':
                self.personaje.ultimo_evento = (
                    "Como Profesor, desactivas la bomba facilmente!"
                )
                for hijo in list(getattr(pos, 'hijos', [])):
                    if getattr(hijo, 'es_bomba', lambda: False)():
                        hijo.activa = False
                self._render()
                time.sleep(1)
            else:
                longitud_bomba = 4 if niebla else 3
                self.personaje.ultimo_evento = (
                    f"BOMBA!{dif_txt} Desactivala con "
                    f"Simon Dice ({longitud_bomba} teclas)"
                )
                self._render()
                msvcrt.getwch()

                evento = EventoSimonDice(
                    longitud=longitud_bomba,
                    mimico=mimico,
                    tiempo_limite=tiempo_evento
                )
                desactivada = evento.ejecutar(self._render_evento)

                if desactivada:
                    self.personaje.ultimo_evento = "Bomba desactivada!"
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

        # ¿Es habitacion tienda?
        es_tienda = self.juego.es_tienda_en(pos)
        if es_tienda:
            self.personaje.ultimo_evento = "Hay un vendedor aqui!"
            self._render()
            msvcrt.getwch()
            tienda = EventoTienda(
                precio=2, nombre_vendedor="Vendedor"
            )
            tienda.ejecutar(self._render_evento, self.personaje)
            self.personaje.ultimo_evento = "Dejaste la tienda."

    # ── Pantallas finales ─────────────────────────────────────────────────────
    def _pantalla_victoria(self):
        """Muestra la pantalla de victoria."""
        _home_cursor()
        lineas = [
            f"╔{_SEP}╗",
            _linea_centrada(""),
            _seccion("*** VICTORIA ***"),
            _linea_centrada(""),
            _linea_centrada(f"{self.personaje.nombre} ha escapado del laberinto!"),
            _linea_centrada(""),
            _linea_centrada(
                f"Clase: {self.personaje.clase.upper()}  "
                f"Dif: {self.personaje.dificultad.upper()}"
            ),
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
        _clear_below()
        msvcrt.getwch()

    def _pantalla_derrota(self):
        """Muestra la pantalla de derrota."""
        _home_cursor()
        lineas = [
            f"╔{_SEP}╗",
            _linea_centrada(""),
            _seccion("*** GAME OVER ***"),
            _linea_centrada(""),
            _linea_centrada(f"{self.personaje.nombre} no ha sobrevivido..."),
            _linea_centrada(
                f"Clase: {self.personaje.clase.upper()}  "
                f"Dif: {self.personaje.dificultad.upper()}"
            ),
            _linea_centrada(""),
            _linea_centrada("Mejor suerte la proxima vez!"),
            _linea_centrada(""),
            _linea_centrada("Pulsa cualquier tecla para salir..."),
            _linea_centrada(""),
            f"╚{_SEP}╝",
        ]
        print("\n".join(lineas))
        _clear_below()
        msvcrt.getwch()

    def _entes_derrotados(self):
        """Cuenta los bichos que ya no están vivos."""
        return sum(1 for b in self.juego.bichos if not b.esta_vivo())

    # ── Bucle principal ───────────────────────────────────────────────────────
    def bucle_principal(self):
        """Lanza el menu y luego el bucle de juego interactivo."""
        # Mostrar menu
        if not self._menu_principal():
            os.system('cls')
            print("Hasta pronto!")
            return

        self.personaje.ultimo_evento = (
            "Bienvenido! Usa WASD o flechas. Llega a la SALIDA."
        )
        self.tiempo_inicio_global = time.time()
        self.tiempo_entrada_sala = time.time()
        self.sala_anterior = self.personaje.posicion
        os.system('cls')  # limpieza inicial unica
        self._render()

        mult = self._mult()

        while self.activo and not self.juego.finalizado:
            # Comprobar timer global
            if self.juego.timer_global:
                tg_real = self.juego.timer_global * mult
                elapsed = time.time() - self.tiempo_inicio_global
                if elapsed >= tg_real:
                    self.personaje.ultimo_evento = (
                        "TIEMPO AGOTADO! Las puertas se cierran!"
                    )
                    self.juego.muere_personaje()
                    break

            # Comprobar timer de sala
            pos = self.personaje.posicion
            if pos and self.juego.hay_temporizador_en(pos):
                seg = self.juego.obtener_tiempo_habitacion(pos)
                seg_real = seg * mult
                elapsed_s = time.time() - self.tiempo_entrada_sala
                if elapsed_s >= seg_real:
                    self.personaje.ultimo_evento = (
                        "Los pinchos bajan! No saliste a tiempo!"
                    )
                    self.personaje.vidas -= 1
                    if self.personaje.vidas <= 0:
                        self.juego.muere_personaje()
                        break
                    # Resetear timer sala
                    self.tiempo_entrada_sala = time.time()
                    self._render()
                    continue

            # Input: usa polling si hay timers activos
            hay_timer_activo = (
                self.juego.timer_global or (
                    pos and self.juego.hay_temporizador_en(pos)
                )
            )

            accion = None
            if hay_timer_activo:
                # Polling no-bloqueante: leer si hay tecla
                if msvcrt.kbhit():
                    accion = self._leer_tecla()
                else:
                    time.sleep(0.1)
                    self._render()  # refrescar para countdown
                    continue
            else:
                accion = self._leer_tecla()

            if accion == 'salir':
                self.activo = False
            elif accion:
                self.personaje.ultimo_evento = ""
                pos_antes = self.personaje.posicion
                self._mover(accion)

                # Detectar cambio de sala => resetear timer
                if self.personaje.posicion != pos_antes:
                    self.tiempo_entrada_sala = time.time()
                    self.sala_anterior = self.personaje.posicion

                # Comprobar eventos en la nueva posicion
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
            print("Hasta pronto!")
