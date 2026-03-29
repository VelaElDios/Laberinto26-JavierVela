"""
Módulo Juego.

Define la clase principal Juego, que actúa como controlador y creador 
del laberinto, y otras clases derivadas como JuegoBombas.
"""
# pylint: disable=invalid-name

import threading
from Orientaciones import Norte, Sur, Este, Oeste
from Formas import Cuadrado
from ElementosMapa import Habitacion, Pared, ParedBomba, Puerta, Laberinto
from Entes import Personaje

class Juego:
    """
    Juego es la clase principal del juego del laberinto
    """
    def __init__(self):
        self.laberinto = None
        self.bichos = []
        self.person = None
        self.hilos = {}

    def abrir_puertas(self):
        # En Smalltalk usa un bloque en el método recorrer
        if self.laberinto:
            self.laberinto.recorrer(lambda each: each.abrir() if each.es_puerta() else None)

    def activar_bombas(self):
        if self.laberinto:
            self.laberinto.recorrer(lambda each: each.activar() if each.es_bomba() else None)

    def agregar_bicho(self, un_bicho):
        self.bichos.append(un_bicho)

    def agregar_personaje(self, una_cadena):
        self.person = Personaje()
        self.person.nombre = una_cadena
        self.person.juego = self
        hab1 = self.obtener_habitacion(1)
        if hab1:
            hab1.entrar(self.person)

    def asignar_orientaciones(self, un_cont):
        if un_cont.forma:
            un_cont.forma.agregar_orientacion(self.fabricar_norte())
            un_cont.forma.agregar_orientacion(self.fabricar_este())
            un_cont.forma.agregar_orientacion(self.fabricar_sur())
            un_cont.forma.agregar_orientacion(self.fabricar_oeste())

    def buscar_personaje(self, un_bicho):
        if getattr(self.person, 'posicion', None) == getattr(un_bicho, 'posicion', None):
            return self.person
        return None

    def cerrar_puertas(self):
        if self.laberinto:
            self.laberinto.recorrer(lambda each: each.cerrar() if each.es_puerta() else None)

    def desactivar_bombas(self):
        if self.laberinto:
            self.laberinto.recorrer(lambda each: each.desactivar() if each.es_bomba() else None)

    def eliminar_bicho(self, un_bicho):
        if un_bicho in self.bichos:
            self.bichos.remove(un_bicho)

    def fabricar_este(self):
        return Este.default()

    def fabricar_habitacion(self):
        return Habitacion()

    def fabricar_habitacion_num(self, un_num):
        hab = Habitacion()
        hab.num = un_num
        hab.forma = Cuadrado()
        
        self.asignar_orientaciones(hab)
        if getattr(hab.forma, 'orientaciones', None):
            for each in hab.forma.orientaciones:
                hab.poner_en_elemento(each, self.fabricar_pared())
        return hab

    def fabricar_lab2_hab(self):
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
        """Crea y configura un laberinto de dos habitaciones conectadas por una puerta, con paredes bomba."""
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
        hab1 = self.fabricar_habitacion_num(1)
        hab2 = self.fabricar_habitacion_num(2)
        puerta = self.fabricar_puerta_lado1_lado2(hab1, hab2)
        
        hab1.poner_en_elemento(self.fabricar_sur(), puerta)
        hab2.poner_en_elemento(self.fabricar_norte(), puerta)
        
        self.laberinto = self.fabricar_laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)

    def fabricar_lab4_hab_fm(self):
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
        return Laberinto()

    def fabricar_norte(self):
        return Norte.default()

    def fabricar_oeste(self):
        return Oeste.default()

    def fabricar_pared(self):
        return Pared()

    def fabricar_puerta(self):
        return Puerta()

    def fabricar_puerta_lado1_lado2(self, una_hab, otra_hab):
        puerta = Puerta()
        puerta.lado1 = una_hab
        puerta.lado2 = otra_hab
        return puerta

    def fabricar_sur(self):
        return Sur.default()

    def lanzar_bicho(self, un_bicho):
        print(f"{un_bicho} se activa")
        def bicho_loop():
            while un_bicho.esta_vivo():
                un_bicho.actua()
                
        thread = threading.Thread(target=bicho_loop, daemon=True)
        self.hilos[un_bicho] = thread
        thread.start()

    def lanzar_todos_los_bichos(self):
        print("Los bichos despiertan")
        for bicho in list(self.bichos):
            self.lanzar_bicho(bicho)

    def muere_bicho(self, un_bicho):
        self.terminar_bicho(un_bicho)

    def muere_personaje(self):
        print("Manmatao. Fin del juego")
        self.terminar_todos_los_bichos()

    def obtener_habitacion(self, un_num):
        if self.laberinto:
            return self.laberinto.obtener_habitacion(un_num)
        return None

    def terminar_bicho(self, un_bicho):
        un_bicho.vidas = 0
        print(f"{un_bicho} muere")

    def terminar_todos_los_bichos(self):
        print("Los bichos terminan")
        for bicho in list(self.bichos):
            self.terminar_bicho(bicho)


class JuegoBombas(Juego):
    """
    JuegoBombas ilustra el patrón FactoryMethod para crear laberintos con paredes-bombas
    """
    def fabricar_pared(self):
        return ParedBomba()


if __name__ == '__main__':
    # Creando el juego basico (Factory Method de la propia clase)
    print("=== INICIALIZANDO JUEGO DE PRUEBA ===")
    juego = Juego()
    juego.fabricar_lab2_hab_fm()
    print("Laberinto construido exitosamente.")
    
    # Añadimos un personaje para ver como entra en la habitacion 1
    juego.agregar_personaje("ProtaPython")
    
    # Recorremos el laberinto
    def debug_bloque(_elem):
        pass # Solo imprime si tiene log
        
    print("-- Recorriendo Elementos --")
    juego.laberinto.recorrer(debug_bloque)
    print("=== FIN PRUEBA ===")
