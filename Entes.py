class Ente:
    """
    Ente es la interfaz de los elementos autonomos del laberinto
    """
    def __init__(self):
        self.poder = 1
        self.posicion = None
        self.vidas = 50
        self.juego = None

    def atacar(self):
        enemigo = self.buscar_enemigo()
        if enemigo:
            enemigo.es_atacado_por(self)

    def buscar_enemigo(self):
        raise NotImplementedError

    def es_atacado_por(self, alguien):
        self.vidas -= alguien.poder
        print(f"{self} es atacado por {alguien}")
        print(f"vidas: {self.vidas}")
        
        if self.vidas <= 0:
            self.muero()

    def esta_vivo(self):
        return self.vidas > 0

    def muero(self):
        raise NotImplementedError


class Personaje(Ente):
    """
    Personaje es el prota del juego
    """
    def __init__(self):
        super().__init__()
        self.nombre = ""

    def buscar_enemigo(self):
        # pedir a juego que me devuelva un bicho en mi posicion
        # En Smalltalk esto estaba comentado, puede dejarse vacío o devolver None
        pass

    def ir_a(self, una_or):
        una_or.caminar(self)

    def ir_al_norte(self):
        if self.posicion:
            self.posicion.ir_al_norte(self)

    def muero(self):
        if self.juego:
            self.juego.muere_personaje()

    def __str__(self):
        return self.nombre


class Bicho(Ente):
    """
    Bicho representa a los enemigos del personaje
    """
    def __init__(self):
        super().__init__()
        self.modo = None

    def actua(self):
        if self.modo:
            self.modo.actua(self)

    def buscar_enemigo(self):
        if self.juego:
            return self.juego.buscar_personaje(self)
        return None

    def es_agresivo(self):
        if self.modo:
            return self.modo.es_agresivo()
        return False

    def es_perezoso(self):
        if self.modo:
            return self.modo.es_perezoso()
        return False

    def muero(self):
        if self.juego:
            self.juego.muere_bicho(self)

    def obtener_orientacion_aleatoria(self):
        if self.posicion:
            return self.posicion.obtener_orientacion_aleatoria()
        return None

    def __str__(self):
        modo_str = str(self.modo) if self.modo else "SinModo"
        return f"Bicho-{modo_str}"
