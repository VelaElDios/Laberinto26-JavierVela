import json
from ElementosMapa import Habitacion, Pared, Puerta, Armario, Laberinto
from Orientaciones import Norte, Sur, Este, Oeste, Noreste, Noroeste, Sureste, Suroeste
from Formas import Cuadrado, Rombo
from Entes import Bicho
from Modos import Agresivo, Perezoso
from Decoradores import Bomba
from Juego import Juego

class LaberintoBuilder:
    """
    LaberintoBuilder es el ConcreteBuilder del patrón Builder
    """
    def __init__(self):
        self.laberinto = None
        self.juego = None

    def asignar_orientaciones(self, una_forma):
        una_forma.agregar_orientacion(self.fabricar_norte())
        una_forma.agregar_orientacion(self.fabricar_este())
        una_forma.agregar_orientacion(self.fabricar_sur())
        una_forma.agregar_orientacion(self.fabricar_oeste())

    def fabricar_agresivo(self):
        return Agresivo()

    def fabricar_armario(self, un_num, un_cont):
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
        bm = Bomba()
        if hasattr(un_cont, 'agregar_hijo'):
            un_cont.agregar_hijo(bm)
        return bm

    def fabricar_este(self):
        return Este.default()

    def fabricar_forma(self):
        forma = Cuadrado()
        self.asignar_orientaciones(forma)
        return forma

    def fabricar_habitacion(self, un_num):
        hab = Habitacion()
        hab.num = un_num
        hab.forma = self.fabricar_forma()
        hab.forma.num = un_num
        
        if hasattr(hab.forma, 'orientaciones'):
            for each in hab.forma.orientaciones:
                hab.poner_en_elemento(each, self.fabricar_pared())
                 
        self.laberinto.agregar_habitacion(hab)
        return hab

    def fabricar_juego(self):
        self.juego = Juego()
        self.juego.laberinto = self.laberinto

    def fabricar_laberinto(self):
        self.laberinto = Laberinto()

    def fabricar_noreste(self):
        return Noreste.default()

    def fabricar_noroeste(self):
        return Noroeste.default()

    def fabricar_norte(self):
        return Norte.default()

    def fabricar_oeste(self):
        return Oeste.default()

    def fabricar_pared(self):
        return Pared()

    def fabricar_perezoso(self):
        return Perezoso()

    def fabricar_puerta_lado1_or1_lado2_or2(self, num1, una_or1, num2, otra_or2):
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
        return Sur.default()

    def fabricar_sureste(self):
        return Sureste.default()

    def fabricar_suroeste(self):
        return Suroeste.default()


class LaberintoBuilderRombo(LaberintoBuilder):
    """
    LaberintoBuilderRombo fabrica laberintos con forma rombo
    """
    def asignar_orientaciones(self, una_forma):
        una_forma.agregar_orientacion(self.fabricar_noreste())
        una_forma.agregar_orientacion(self.fabricar_noroeste())
        una_forma.agregar_orientacion(self.fabricar_sureste())
        una_forma.agregar_orientacion(self.fabricar_suroeste())

    def fabricar_forma(self):
        forma = Rombo()
        self.asignar_orientaciones(forma)
        return forma


class Director:
    """
    Director representa al director del patrón Builder
    """
    def __init__(self):
        self.builder = None
        self.data_dict = {}

    def fabricar_bichos(self):
        bichos = self.data_dict.get('bichos', [])
        for each in bichos:
            self.builder.fabricar_bicho_modo(each.get('modo'), each.get('posicion'))

    def fabricar_juego(self):
        self.builder.fabricar_juego()

    def fabricar_laberinto(self):
        self.builder.fabricar_laberinto()
        
        lab_nodes = self.data_dict.get('laberinto', [])
        for each in lab_nodes:
            self.fabricar_laberinto_recursivo(each, None)
             
        puertas = self.data_dict.get('puertas', [])
        for pt_data in puertas:
            # pt_data se asume como una lista [num1, or1, num2, or2]
            if len(pt_data) >= 4:
                self.builder.fabricar_puerta_lado1_or1_lado2_or2(pt_data[0], pt_data[1], pt_data[2], pt_data[3])

    def fabricar_laberinto_recursivo(self, un_dic, padre):
        tipo = un_dic.get('tipo', '')
        num = un_dic.get('num')
        con = None
        
        if tipo == 'habitacion':
            con = self.builder.fabricar_habitacion(num)
        elif tipo == 'armario':
            con = self.builder.fabricar_armario(num, padre)
        elif tipo == 'bomba':
            con = self.builder.fabricar_bomba_en(padre)
             
        hijos = un_dic.get('hijos', [])
        for each in hijos:
            self.fabricar_laberinto_recursivo(each, con)

    def ini_builder(self):
        forma_val = self.data_dict.get('forma')
        if forma_val == 'poligono4':
            self.builder = LaberintoBuilder()
        elif forma_val == 'rombo':
            self.builder = LaberintoBuilderRombo()

    def leer_archivo(self, un_archivo):
        with open(un_archivo, 'r', encoding='utf-8') as file:
            self.data_dict = json.load(file)

    def obtener_juego(self):
        return self.builder.juego if self.builder else None

    def procesar(self, un_archivo):
        self.leer_archivo(un_archivo)
        self.ini_builder()
        self.fabricar_laberinto()
        self.fabricar_juego()
        self.fabricar_bichos()
