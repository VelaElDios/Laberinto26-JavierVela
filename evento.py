"""
Modulo evento.

Define los minijuegos (eventos) que se activan al interactuar con
elementos del laberinto: Simon Dice para bombas y Piedra-Papel-Tijeras
para combate contra entes. Incluye modo mimico que invierte reglas.
"""
import random
import sys
import msvcrt

# Forzar UTF-8 en la salida
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (OSError, ValueError):
        pass


# ─── Utilidades de input ─────────────────────────────────────────────────────
def _leer_tecla_evento():
    """Lee una tecla sin necesidad de pulsar Enter (msvcrt)."""
    ch = msvcrt.getwch()
    if ch in ('\xe0', '\x00'):
        msvcrt.getwch()       # descarta segundo byte de tecla especial
        return None
    return ch.lower()


def _leer_tecla_con_timeout(deadline):
    """
    Lee una tecla con timeout. Devuelve la tecla o None si se
    acaba el tiempo. deadline es un time.time() absoluto.
    """
    import time
    while time.time() < deadline:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ('\xe0', '\x00'):
                msvcrt.getwch()
                continue
            return ch.lower()
        time.sleep(0.05)  # polling cada 50ms
    return None  # timeout


# ─── Piedra Papel Tijeras ────────────────────────────────────────────────────
class EventoPPT:
    """
    Evento Piedra-Papel-Tijeras.
    El jugador tiene 3 vidas (o 2 en niebla), el ente tiene 1 vida.
    Las vidas se resetean en cada combate nuevo.
    Controles: R=Piedra, P=Papel, T=Tijeras

    Modo mimico: las reglas se invierten.
    Normal:  Piedra>Tijera, Tijera>Papel, Papel>Piedra
    Mimico:  Tijera>Piedra, Piedra>Papel, Papel>Tijera
    """

    OPCIONES = {'r': 'PIEDRA', 'p': 'PAPEL', 't': 'TIJERAS'}
    # Normal: clave gana a valor
    GANA_NORMAL = {'r': 't', 'p': 'r', 't': 'p'}
    # Mimico: todo invertido
    GANA_MIMICO = {'t': 'r', 'r': 'p', 'p': 't'}

    def __init__(self, mimico=False, tiempo_limite=None):
        self.vidas_jugador = 3
        self.vidas_ente = 1
        self.mimico = mimico
        self.tiempo_limite = tiempo_limite  # segundos o None
        self.tabla_gana = self.GANA_MIMICO if mimico else self.GANA_NORMAL

    def ejecutar(self, render_fn):
        """
        Ejecuta el minijuego.
        render_fn(lineas: list[str]) se usa para dibujar en pantalla.
        Devuelve True si el jugador gana, False si pierde.
        """
        max_vidas = self.vidas_jugador
        self.vidas_ente = 1
        modo_txt = " [MIMICO!]" if self.mimico else ""
        timer_txt = f" ({self.tiempo_limite}s)" if self.tiempo_limite else ""

        import time
        deadline = (time.time() + self.tiempo_limite) if self.tiempo_limite else None

        while self.vidas_jugador > 0 and self.vidas_ente > 0:
            # Check timeout
            if deadline and time.time() >= deadline:
                return False  # se acabo el tiempo

            restante = int(deadline - time.time()) if deadline else None
            v_j = "O" * self.vidas_jugador + "." * (max_vidas - self.vidas_jugador)
            v_e = "O" * self.vidas_ente
            lineas = [
                f"====== COMBATE{modo_txt}{timer_txt} ======",
                "",
            ]
            if restante is not None:
                lineas.append(f"  TIEMPO: {restante}s")
            lineas.extend([
                f"  Tus vidas:  [{v_j}]",
                f"  Ente vidas: [{v_e}]",
                "",
                "  [R] Piedra",
                "  [P] Papel",
                "  [T] Tijeras",
                "",
            ])
            if self.mimico:
                lineas.append("  (REGLAS INVERTIDAS!)")
            lineas.append("  Elige tu jugada:")
            render_fn(lineas)

            # Leer input (con o sin timeout)
            eleccion = None
            while eleccion not in self.OPCIONES:
                if deadline:
                    eleccion = _leer_tecla_con_timeout(deadline)
                    if eleccion is None:
                        return False  # timeout
                else:
                    eleccion = _leer_tecla_evento()

            cpu = random.choice(list(self.OPCIONES.keys()))
            nombre_j = self.OPCIONES[eleccion]
            nombre_c = self.OPCIONES[cpu]

            if eleccion == cpu:
                resultado = "EMPATE"
            elif self.tabla_gana[eleccion] == cpu:
                resultado = "GANASTE la ronda!"
                self.vidas_ente -= 1
            else:
                resultado = "PERDISTE la ronda"
                self.vidas_jugador -= 1

            v_j = "O" * self.vidas_jugador + "." * (max_vidas - self.vidas_jugador)
            v_e = "O" * self.vidas_ente
            lineas_res = [
                f"====== COMBATE{modo_txt} ======",
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
    Controles: W, A, S, D

    Modo mimico: los controles se invierten.
    W(arriba)=S(abajo), S(abajo)=W(arriba),
    A(izquierda)=D(derecha), D(derecha)=A(izquierda)
    """

    TECLAS = ['w', 'a', 's', 'd']
    NOMBRES_NORMAL = {'w': '^W', 'a': '<A', 's': 'vS', 'd': '>D'}
    # Mimico: los controles se muestran normal pero se invierten al pulsar
    INVERSION = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}

    def __init__(self, longitud=3, mimico=False, tiempo_limite=None):
        self.longitud = longitud
        self.mimico = mimico
        self.tiempo_limite = tiempo_limite  # segundos o None

    def _traducir_tecla(self, tecla):
        """Invierte la tecla si es modo mimico."""
        if self.mimico and tecla in self.INVERSION:
            return self.INVERSION[tecla]
        return tecla

    def ejecutar(self, render_fn):
        """
        Ejecuta el minijuego.
        Devuelve True si desactiva la bomba, False si explota.
        """
        import time

        secuencia = [random.choice(self.TECLAS)
                     for _ in range(self.longitud)]
        nombres_seq = ' '.join(
            self.NOMBRES_NORMAL[t] for t in secuencia
        )
        modo_txt = " [MIMICO!]" if self.mimico else ""
        timer_txt = f" ({self.tiempo_limite}s)" if self.tiempo_limite else ""

        # Mostrar secuencia
        lineas = [
            f"====== BOMBA{modo_txt}{timer_txt} ======",
            "",
            "  Desactiva la bomba!",
            "  Memoriza la secuencia:",
            "",
            f"    {nombres_seq}",
            "",
        ]
        if self.mimico:
            lineas.append("  (CONTROLES INVERTIDOS!)")
            lineas.append("  ^=v, v=^, <=>, >=<")
        lineas.extend([
            "",
            "  Pulsa cualquier tecla",
            "  cuando estes listo...",
        ])
        render_fn(lineas)
        _leer_tecla_evento()

        # Deadline para el timer
        deadline = (time.time() + self.tiempo_limite) if self.tiempo_limite else None

        # Pedir repeticion
        aciertos = 0
        for i, tecla_correcta in enumerate(secuencia):
            if deadline and time.time() >= deadline:
                return False  # timeout

            restantes = self.longitud - i
            restante_t = int(deadline - time.time()) if deadline else None
            lineas_input = [
                f"====== BOMBA{modo_txt}{timer_txt} ======",
                "",
            ]
            if restante_t is not None:
                lineas_input.append(f"  TIEMPO: {restante_t}s")
            lineas_input.extend([
                f"  Paso {i + 1}/{self.longitud}",
                f"  Teclas restantes: {restantes}",
                "",
                "  Pulsa la tecla correcta",
                "  (W / A / S / D):",
            ])
            if self.mimico:
                lineas_input.append("  (INVERTIDO!)")
            render_fn(lineas_input)

            tecla = None
            while tecla not in self.TECLAS:
                if deadline:
                    tecla = _leer_tecla_con_timeout(deadline)
                    if tecla is None:
                        return False  # timeout
                else:
                    tecla = _leer_tecla_evento()

            # En mimico, la tecla pulsada se invierte
            tecla_real = self._traducir_tecla(tecla)

            if tecla_real == tecla_correcta:
                aciertos += 1
            else:
                nombre_correcta = self.NOMBRES_NORMAL[tecla_correcta]
                lineas_fallo = [
                    f"====== BOMBA{modo_txt} ======",
                    "",
                    f"  INCORRECTO! Era {nombre_correcta}",
                    "  ** LA BOMBA HA EXPLOTADO! **",
                    "",
                    "  Pulsa cualquier tecla...",
                ]
                render_fn(lineas_fallo)
                _leer_tecla_evento()
                return False

        lineas_ok = [
            f"====== BOMBA{modo_txt} ======",
            "",
            "  BOMBA DESACTIVADA!",
            f"  {aciertos}/{self.longitud} aciertos",
            "",
            "  Pulsa cualquier tecla...",
        ]
        render_fn(lineas_ok)
        _leer_tecla_evento()
        return True


# ─── Tienda ──────────────────────────────────────────────────────────────────
class EventoTienda:
    """
    Evento de tienda: permite comprar vidas con sangre.
    Se muestra al entrar en una HabitacionTienda o al encontrar
    un ente perezoso.
    """

    def __init__(self, precio=2, nombre_vendedor="Vendedor"):
        self.precio = precio
        self.nombre_vendedor = nombre_vendedor

    def ejecutar(self, render_fn, personaje):
        """
        Ejecuta el minijuego de tienda.
        El jugador puede comprar vidas o salir.
        Guerrero puede comprar espada.
        """
        precio_espada = 3

        while True:
            lineas = [
                "====== TIENDA ======",
                "",
                f"  {self.nombre_vendedor}:",
                "  'Tengo cosas a la venta...'",
                "",
                f"  Tu sangre: {personaje.sangre}",
                f"  Tus vidas: {personaje.vidas}",
                "",
                f"  [C] Comprar 1 vida ({self.precio} sangre)",
            ]
            # Opcion espada solo para guerrero sin espada
            puede_espada = (
                getattr(personaje, 'clase', '') == 'guerrero'
                and not getattr(personaje, 'tiene_espada', False)
            )
            if puede_espada:
                lineas.append(
                    f"  [E] Comprar Espada ({precio_espada} sangre)"
                )
            lineas.extend([
                "  [Q] Salir de la tienda",
                "",
            ])
            render_fn(lineas)

            teclas_validas = ['c', 'q']
            if puede_espada:
                teclas_validas.append('e')

            tecla = None
            while tecla not in teclas_validas:
                tecla = _leer_tecla_evento()

            if tecla == 'q':
                return

            if tecla == 'c':
                if personaje.sangre >= self.precio:
                    personaje.sangre -= self.precio
                    personaje.vidas += 1
                    lineas_ok = [
                        "====== TIENDA ======",
                        "",
                        f"  {self.nombre_vendedor}:",
                        "  'Trato hecho!'",
                        "",
                        f"  +1 vida! Vidas: {personaje.vidas}",
                        f"  Sangre restante: {personaje.sangre}",
                        "",
                        "  Pulsa cualquier tecla...",
                    ]
                    render_fn(lineas_ok)
                    _leer_tecla_evento()
                else:
                    lineas_no = [
                        "====== TIENDA ======",
                        "",
                        f"  {self.nombre_vendedor}:",
                        "  'No tienes suficiente sangre.'",
                        f"  (Necesitas {self.precio}, "
                        f"tienes {personaje.sangre})",
                        "",
                        "  Pulsa cualquier tecla...",
                    ]
                    render_fn(lineas_no)
                    _leer_tecla_evento()

            if tecla == 'e' and puede_espada:
                if personaje.sangre >= precio_espada:
                    personaje.sangre -= precio_espada
                    personaje.tiene_espada = True
                    lineas_ok = [
                        "====== TIENDA ======",
                        "",
                        f"  {self.nombre_vendedor}:",
                        "  'Una espada magnifica!'",
                        "",
                        "  Has obtenido la ESPADA!",
                        "  Los enemigos caen ante ti.",
                        f"  Sangre restante: {personaje.sangre}",
                        "",
                        "  Pulsa cualquier tecla...",
                    ]
                    render_fn(lineas_ok)
                    _leer_tecla_evento()
                else:
                    lineas_no = [
                        "====== TIENDA ======",
                        "",
                        f"  {self.nombre_vendedor}:",
                        "  'No tienes suficiente sangre.'",
                        f"  (Necesitas {precio_espada}, "
                        f"tienes {personaje.sangre})",
                        "",
                        "  Pulsa cualquier tecla...",
                    ]
                    render_fn(lineas_no)
                    _leer_tecla_evento()

