class ElementoMapa:
    """
    ElementoMapa es la interfaz común de los elementos del laberinto
    """
    def entrar(self, alguien):
        raise NotImplementedError

    def es_bomba(self):
        return False

    def es_puerta(self):
        return False

    def recorrer(self, un_bloque):
        raise NotImplementedError


class Hoja(ElementoMapa):
    """
    Es la interfaz de los elementos simples del laberinto (es Leaf en el patrón Composite)
    """
    def entrar(self, alguien):
        raise NotImplementedError

    def recorrer(self, un_bloque):
        print(str(self))
        un_bloque(self)


class Contenedor(ElementoMapa):
    """
    Es un elemento del mapa que tiene hijos (es el compuesto del patrón Composite)
    """
    def __init__(self):
        self.hijos = []
        self.forma = None
        self.num = None

    def agregar_hijo(self, un_em):
        self.hijos.append(un_em)

    def agregar_orientacion(self, una_or):
        if self.forma:
            self.forma.agregar_orientacion(una_or)

    def eliminar_hijo(self, un_em):
        if un_em in self.hijos:
            self.hijos.remove(un_em)

    def eliminar_orientacion(self, una_or):
        if self.forma:
            self.forma.eliminar_orientacion(una_or)

    def entrar(self, alguien):
        alguien.posicion = self
        msg = f"Estás en {self}."
        if hasattr(alguien, 'ultimo_evento'):
            alguien.ultimo_evento = msg
        else:
            print(f"{alguien} está en {self}")

    def ir_al_norte(self, alguien):
        if self.forma:
            self.forma.ir_al_norte(alguien)

    def obtener_orientacion_aleatoria(self):
        if self.forma:
            return self.forma.obtener_orientacion_aleatoria()
        return None

    def poner_en_elemento(self, una_or, un_em):
        if self.forma:
            self.forma.poner_en_elemento(una_or, un_em)

    def recorrer(self, un_bloque):
        print(str(self))
        un_bloque(self)
        for hijo in self.hijos:
            hijo.recorrer(un_bloque)
        
        if self.forma and hasattr(self.forma, 'orientaciones'):
            for orien in self.forma.orientaciones:
                orien.recorrer_en_contenedor(un_bloque, self.forma)


class Pared(Hoja):
    """
    Pared es un elemento del mapa que no se puede atravesar
    """
    def entrar(self, alguien):
        msg = "¡Chocaste con una pared!"
        if alguien and hasattr(alguien, 'ultimo_evento'):
            alguien.ultimo_evento = msg
        else:
            print(msg)

    def __str__(self):
        return "Pared"


class ParedBomba(Pared):
    """
    ParedBomba es una pared que tiene una bomba
    """
    def __init__(self):
        super().__init__()
        self.activa = False


class Habitacion(Contenedor):
    """
    Es un contenedor (es elemento mapa)
    """
    def entrar(self, alguien):
        alguien.posicion = self
        msg = f"Has entrado en {self}."
        if hasattr(alguien, 'ultimo_evento'):
            alguien.ultimo_evento = msg
        else:
            print(f"{alguien} está en {self}")

    def __str__(self):
        return f"Hab-{self.num}"


class Laberinto(Contenedor):
    """
    Laberinto es un EM que tiene habitaciones
    """
    def agregar_habitacion(self, una_hab):
        self.agregar_hijo(una_hab)

    def entrar(self, alguien):
        hab = self.obtener_habitacion(1)
        if hab:
            hab.entrar(alguien)

    def obtener_habitacion(self, un_num):
        for hijo in self.hijos:
            if getattr(hijo, 'num', None) == un_num:
                return hijo
        return None

    def recorrer(self, un_bloque):
        print("Recorriendo el laberinto")
        for hijo in self.hijos:
            hijo.recorrer(un_bloque)


class Puerta(Hoja):
    """
    Puerta es un elemento del mapa que une dos habitaciones y tiene abierta 
    """
    def __init__(self):
        super().__init__()
        self.abierta = False
        self.lado1 = None
        self.lado2 = None

    def abrir(self):
        print(f"Abrimos {self}")
        self.abierta = True

    def cerrar(self):
        print(f"Cerramos {self}")
        self.abierta = False

    def entrar(self, alguien):
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
        return True

    def __str__(self):
        return f"Puerta-{getattr(self.lado1, 'num', 'None')}-{getattr(self.lado2, 'num', 'None')}"


class Armario(Contenedor):
    """
    Armario es un contenedor que tiene una puerta al este
    """
