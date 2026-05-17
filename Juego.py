"""
Módulo juego.

Define la clase Juego, controlador principal del laberinto.
Implementa el patrón Factory Method con los métodos fabricar_*.
"""
import threading
from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from cuadrado import Cuadrado
from habitacion import Habitacion
from pared import Pared
from pared_bomba import ParedBomba
from puerta import Puerta
from laberinto import Laberinto
from personaje import Personaje


class JuegoError(Exception):
    """Excepción base para errores del juego."""


class JuegoFinalizadoError(JuegoError):
    """Se lanza cuando se intenta actuar en un juego ya finalizado."""


class Juego:
    """
    Juego es la clase principal del juego del laberinto.
    Implementa el patrón Factory Method: las subclases pueden sobreescribir
    los métodos fabricar_* para crear variantes del laberinto.
    """

    def __init__(self):
        self.laberinto = None
        self.bichos = []
        self.person = None
        self.hilos = {}
        self.finalizado = False
        self.resultado = None
        self.callback_fin = lambda: None

    def abrir_puertas(self):
        """Abre todas las puertas del laberinto."""
        if self.laberinto:
            self.laberinto.recorrer(lambda each: each.abrir() if each.es_puerta() else None)

    def activar_bombas(self):
        """Activa todas las bombas del laberinto."""
        if self.laberinto:
            self.laberinto.recorrer(lambda each: each.activar() if each.es_bomba() else None)

    def agregar_bicho(self, un_bicho):
        """Añade un bicho a la lista de bichos del juego."""
        self.bichos.append(un_bicho)

    def agregar_personaje(self, una_cadena):
        """Crea un personaje con el nombre dado y lo coloca en la habitación 1."""
        self.person = Personaje()
        self.person.nombre = una_cadena
        self.person.juego = self
        hab1 = self.obtener_habitacion(1)
        if hab1:
            hab1.entrar(self.person)

    def asignar_orientaciones(self, un_cont):
        """Añade las cuatro orientaciones cardinales a la forma del contenedor."""
        if un_cont.forma:
            un_cont.forma.agregar_orientacion(self.fabricar_norte())
            un_cont.forma.agregar_orientacion(self.fabricar_este())
            un_cont.forma.agregar_orientacion(self.fabricar_sur())
            un_cont.forma.agregar_orientacion(self.fabricar_oeste())

    def buscar_personaje(self, un_bicho):
        """Devuelve el personaje si está en la misma posición que el bicho."""
        if getattr(self.person, 'posicion', None) == getattr(un_bicho, 'posicion', None):
            return self.person
        return None

    def cerrar_puertas(self):
        """Cierra todas las puertas del laberinto."""
        if self.laberinto:
            self.laberinto.recorrer(lambda each: each.cerrar() if each.es_puerta() else None)

    def desactivar_bombas(self):
        """Desactiva todas las bombas del laberinto."""
        if self.laberinto:
            self.laberinto.recorrer(lambda each: each.desactivar() if each.es_bomba() else None)

    def eliminar_bicho(self, un_bicho):
        """Elimina un bicho de la lista."""
        if un_bicho in self.bichos:
            self.bichos.remove(un_bicho)

    def fabricar_este(self):
        """Devuelve la instancia Singleton de Este."""
        return Este.default()

    def fabricar_habitacion(self):
        """Crea una habitación vacía."""
        return Habitacion()

    def fabricar_habitacion_num(self, un_num):
        """Crea una habitación numerada con forma cuadrada y paredes."""
        hab = Habitacion()
        hab.num = un_num
        hab.forma = Cuadrado()
        self.asignar_orientaciones(hab)
        if getattr(hab.forma, 'orientaciones', None):
            for each in hab.forma.orientaciones:
                hab.poner_en_elemento(each, self.fabricar_pared())
        return hab

    def fabricar_lab2_hab(self):
        """Construye un laberinto básico de 2 habitaciones."""
        hab1 = Habitacion()
        hab1.num = 1
        hab2 = Habitacion()
        hab2.num = 2
        puerta = Puerta()
        puerta.lado1 = hab1
        puerta.lado2 = hab2
        hab1.sur = puerta
        hab2.norte = puerta
        hab1.este = Pared()
        hab1.oeste = Pared()
        hab1.norte = Pared()
        hab2.este = Pared()
        hab2.oeste = Pared()
        hab2.sur = Pared()
        self.laberinto = Laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)

    def fabricar_lab2_hab_bomba(self):
        """Construye un laberinto de 2 habitaciones con paredes bomba."""
        hab1 = Habitacion()
        hab1.num = 1
        hab2 = Habitacion()
        hab2.num = 2
        puerta = Puerta()
        puerta.lado1 = hab1
        puerta.lado2 = hab2
        hab1.sur = puerta
        hab2.norte = puerta
        hab1.este = ParedBomba()
        hab1.oeste = ParedBomba()
        hab1.norte = ParedBomba()
        hab2.este = ParedBomba()
        hab2.oeste = ParedBomba()
        hab2.sur = ParedBomba()
        self.laberinto = Laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)

    def fabricar_lab2_hab_fm(self):
        """Construye un laberinto de 2 habitaciones usando Factory Methods."""
        hab1 = self.fabricar_habitacion_num(1)
        hab2 = self.fabricar_habitacion_num(2)
        puerta = self.fabricar_puerta_lado1_lado2(hab1, hab2)
        hab1.poner_en_elemento(self.fabricar_sur(), puerta)
        hab2.poner_en_elemento(self.fabricar_norte(), puerta)
        self.laberinto = self.fabricar_laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)

    def fabricar_lab4_hab_fm(self):
        """Construye un laberinto de 4 habitaciones usando Factory Methods."""
        hab1 = self.fabricar_habitacion_num(1)
        hab2 = self.fabricar_habitacion_num(2)
        hab3 = self.fabricar_habitacion_num(3)
        hab4 = self.fabricar_habitacion_num(4)
        p12 = self.fabricar_puerta_lado1_lado2(hab1, hab2)
        p13 = self.fabricar_puerta_lado1_lado2(hab1, hab3)
        p24 = self.fabricar_puerta_lado1_lado2(hab2, hab4)
        p34 = self.fabricar_puerta_lado1_lado2(hab3, hab4)
        hab1.poner_en_elemento(self.fabricar_sur(), p12)
        hab2.poner_en_elemento(self.fabricar_norte(), p12)
        hab1.poner_en_elemento(self.fabricar_este(), p13)
        hab3.poner_en_elemento(self.fabricar_oeste(), p13)
        hab2.poner_en_elemento(self.fabricar_este(), p24)
        hab4.poner_en_elemento(self.fabricar_oeste(), p24)
        hab3.poner_en_elemento(self.fabricar_sur(), p34)
        hab4.poner_en_elemento(self.fabricar_norte(), p34)
        self.laberinto = self.fabricar_laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)
        self.laberinto.agregar_habitacion(hab3)
        self.laberinto.agregar_habitacion(hab4)

    def fabricar_laberinto(self):
        """Crea y devuelve un Laberinto vacío."""
        return Laberinto()

    def fabricar_norte(self):
        """Devuelve la instancia Singleton de Norte."""
        return Norte.default()

    def fabricar_oeste(self):
        """Devuelve la instancia Singleton de Oeste."""
        return Oeste.default()

    def fabricar_pared(self):
        """Crea y devuelve una Pared."""
        return Pared()

    def fabricar_puerta(self):
        """Crea y devuelve una Puerta."""
        return Puerta()

    def fabricar_puerta_lado1_lado2(self, una_hab, otra_hab):
        """Crea una puerta que conecta dos habitaciones."""
        puerta = Puerta()
        puerta.lado1 = una_hab
        puerta.lado2 = otra_hab
        return puerta

    def fabricar_sur(self):
        """Devuelve la instancia Singleton de Sur."""
        return Sur.default()

    def gana_personaje(self):
        """El personaje ha ganado la partida. Marca fin de juego."""
        self.finalizado = True
        self.resultado = "victoria"
        self.terminar_todos_los_bichos()
        self.callback_fin()

    def hay_bichos_en(self, habitacion):
        """Devuelve la lista de bichos vivos en la habitación dada."""
        return [b for b in self.bichos
                if b.esta_vivo() and getattr(b, 'posicion', None) == habitacion]

    def hay_bombas_en(self, habitacion):
        """Devuelve True si la habitación tiene bombas activas como hijos."""
        for hijo in getattr(habitacion, 'hijos', []):
            if getattr(hijo, 'es_bomba', lambda: False)():
                if getattr(hijo, 'activa', False):
                    return True
        return False

    def lanzar_bicho(self, un_bicho):
        """Lanza un bicho en un hilo de ejecución propio."""
        print(f"{un_bicho} se activa")

        def bicho_loop():
            while un_bicho.esta_vivo():
                try:
                    un_bicho.actua()
                except (AttributeError, TypeError) as exc:
                    print(f"Error en bicho {un_bicho}: {exc}")
                    break

        thread = threading.Thread(target=bicho_loop, daemon=True)
        self.hilos[un_bicho] = thread
        thread.start()

    def lanzar_todos_los_bichos(self):
        """Lanza todos los bichos del juego."""
        print("Los bichos despiertan")
        for bicho in list(self.bichos):
            self.lanzar_bicho(bicho)

    def muere_bicho(self, un_bicho):
        """Gestiona la muerte de un bicho."""
        self.terminar_bicho(un_bicho)

    def muere_personaje(self):
        """Gestiona la muerte del personaje. Marca fin de juego."""
        self.finalizado = True
        self.resultado = "derrota"
        self.terminar_todos_los_bichos()
        self.callback_fin()

    def obtener_habitacion(self, un_num):
        """Devuelve la habitación con el número indicado."""
        if self.laberinto:
            return self.laberinto.obtener_habitacion(un_num)
        return None

    def terminar_bicho(self, un_bicho):
        """Termina la vida de un bicho."""
        un_bicho.vidas = 0
        print(f"{un_bicho} muere")

    def terminar_todos_los_bichos(self):
        """Termina la vida de todos los bichos."""
        print("Los bichos terminan")
        for bicho in list(self.bichos):
            self.terminar_bicho(bicho)
