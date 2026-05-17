"""
Módulo laberinto_builder.

Define la clase LaberintoBuilder, ConcreteBuilder del patrón Builder
para laberintos con habitaciones cuadradas.
"""
from habitacion import Habitacion
from habitacion_salida import HabitacionSalida
from pared import Pared
from puerta import Puerta
from armario import Armario
from laberinto import Laberinto
from cuadrado import Cuadrado
from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from noreste import Noreste
from noroeste import Noroeste
from sureste import Sureste
from suroeste import Suroeste
from bicho import Bicho
from agresivo import Agresivo
from perezoso import Perezoso
from bomba import Bomba
from niebla import Niebla
from mimico import Mimico
from habitacion_tienda import HabitacionTienda
from temporizador import Temporizador
from juego import Juego


class LaberintoBuilder:
    """
    LaberintoBuilder es el ConcreteBuilder del patrón Builder.
    Construye laberintos con habitaciones de forma cuadrada.
    """

    def __init__(self):
        self.laberinto = None
        self.juego = None

    def asignar_orientaciones(self, una_forma):
        """Asigna las cuatro orientaciones cardinales a una forma."""
        una_forma.agregar_orientacion(self.fabricar_norte())
        una_forma.agregar_orientacion(self.fabricar_este())
        una_forma.agregar_orientacion(self.fabricar_sur())
        una_forma.agregar_orientacion(self.fabricar_oeste())

    def fabricar_agresivo(self):
        """Crea un modo Agresivo."""
        return Agresivo()

    def fabricar_armario(self, un_num, un_cont):
        """Crea un armario numerado dentro de un contenedor padre."""
        arm = Armario()
        arm.num = un_num
        self.asignar_orientaciones(arm)

        for each in getattr(arm, 'orientaciones', []):
            arm.poner_en_elemento(each, self.fabricar_pared())

        pt = Puerta()
        pt.lado1 = arm
        pt.lado2 = un_cont

        arm.poner_en_elemento(self.fabricar_este(), pt)
        if hasattr(un_cont, 'agregar_hijo'):
            un_cont.agregar_hijo(arm)

        return arm

    def fabricar_bicho_modo(self, str_modo, un_num):
        """Crea un bicho con el modo indicado y lo coloca en la habitación."""
        modo_func = getattr(self, "fabricar_" + str_modo.lower())
        modo = modo_func()
        hab = self.juego.obtener_habitacion(un_num)

        bicho = Bicho()
        bicho.modo = modo
        if hab:
            hab.entrar(bicho)

        self.juego.agregar_bicho(bicho)
        bicho.juego = self.juego

    def fabricar_bomba_en(self, un_cont):
        """Crea una bomba dentro de un contenedor."""
        bm = Bomba()
        if hasattr(un_cont, 'agregar_hijo'):
            un_cont.agregar_hijo(bm)
        return bm

    def fabricar_este(self):
        """Devuelve la instancia Singleton de Este."""
        return Este.default()

    def fabricar_forma(self):
        """Crea una forma cuadrada con orientaciones asignadas."""
        forma = Cuadrado()
        self.asignar_orientaciones(forma)
        return forma

    def fabricar_habitacion(self, un_num):
        """Crea una habitación numerada y la añade al laberinto."""
        hab = Habitacion()
        hab.num = un_num
        hab.forma = self.fabricar_forma()
        hab.forma.num = un_num

        if hasattr(hab.forma, 'orientaciones'):
            for each in hab.forma.orientaciones:
                hab.poner_en_elemento(each, self.fabricar_pared())

        self.laberinto.agregar_habitacion(hab)
        return hab

    def fabricar_habitacion_salida(self, un_num):
        """Crea una habitación de salida numerada y la añade al laberinto."""
        hab = HabitacionSalida()
        hab.num = un_num
        hab.forma = self.fabricar_forma()
        hab.forma.num = un_num

        if hasattr(hab.forma, 'orientaciones'):
            for each in hab.forma.orientaciones:
                hab.poner_en_elemento(each, self.fabricar_pared())

        self.laberinto.agregar_habitacion(hab)
        return hab

    def fabricar_bomba_en_habitacion(self, un_num):
        """Crea una bomba activa dentro de la habitación indicada."""
        hab = self.laberinto.obtener_habitacion(un_num)
        if hab:
            bm = Bomba()
            bm.activa = True
            hab.agregar_hijo(bm)
            return bm
        return None

    def fabricar_niebla_en_habitacion(self, un_num):
        """Coloca niebla activa dentro de la habitacion indicada."""
        hab = self.laberinto.obtener_habitacion(un_num)
        if hab:
            nb = Niebla()
            nb.activa = True
            hab.agregar_hijo(nb)
            return nb
        return None

    def fabricar_mimico_en_habitacion(self, un_num):
        """Coloca un mimico activo dentro de la habitacion indicada."""
        hab = self.laberinto.obtener_habitacion(un_num)
        if hab:
            mm = Mimico()
            mm.activa = True
            hab.agregar_hijo(mm)
            return mm
        return None

    def fabricar_temporizador_en_habitacion(self, un_num, segundos=60):
        """Coloca un temporizador en la habitacion indicada."""
        hab = self.laberinto.obtener_habitacion(un_num)
        if hab:
            tp = Temporizador(segundos=segundos)
            tp.activa = True
            hab.agregar_hijo(tp)
            return tp
        return None

    def fabricar_habitacion_tienda(self, un_num):
        """Crea una HabitacionTienda con el numero dado."""
        hab = HabitacionTienda()
        hab.num = un_num
        hab.forma = self.fabricar_forma()
        hab.forma.num = un_num

        if hasattr(hab.forma, 'orientaciones'):
            for each in hab.forma.orientaciones:
                hab.poner_en_elemento(each, self.fabricar_pared())

        self.laberinto.agregar_habitacion(hab)
        return hab

    def fabricar_juego(self):
        """Crea el objeto Juego y lo asocia al laberinto."""
        self.juego = Juego()
        self.juego.laberinto = self.laberinto

    def fabricar_laberinto(self):
        """Inicializa el laberinto."""
        self.laberinto = Laberinto()

    def fabricar_noreste(self):
        """Devuelve la instancia Singleton de Noreste."""
        return Noreste.default()

    def fabricar_noroeste(self):
        """Devuelve la instancia Singleton de Noroeste."""
        return Noroeste.default()

    def fabricar_norte(self):
        """Devuelve la instancia Singleton de Norte."""
        return Norte.default()

    def fabricar_oeste(self):
        """Devuelve la instancia Singleton de Oeste."""
        return Oeste.default()

    def fabricar_pared(self):
        """Crea y devuelve una Pared."""
        return Pared()

    def fabricar_perezoso(self):
        """Crea un modo Perezoso."""
        return Perezoso()

    def fabricar_puerta_lado1_or1_lado2_or2(self, num1, una_or1, num2, otra_or2):
        """Crea una puerta entre dos habitaciones en las orientaciones indicadas."""
        pt = Puerta()
        lado1 = self.laberinto.obtener_habitacion(num1)
        lado2 = self.laberinto.obtener_habitacion(num2)

        pt.lado1 = lado1
        pt.lado2 = lado2

        obj_or1 = getattr(self, "fabricar_" + una_or1.lower())()
        obj_or2 = getattr(self, "fabricar_" + otra_or2.lower())()

        if lado1:
            lado1.poner_en_elemento(obj_or1, pt)
        if lado2:
            lado2.poner_en_elemento(obj_or2, pt)

    def fabricar_sur(self):
        """Devuelve la instancia Singleton de Sur."""
        return Sur.default()

    def fabricar_sureste(self):
        """Devuelve la instancia Singleton de Sureste."""
        return Sureste.default()

    def fabricar_suroeste(self):
        """Devuelve la instancia Singleton de Suroeste."""
        return Suroeste.default()
