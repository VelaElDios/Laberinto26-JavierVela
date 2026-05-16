"""
Módulo director.

Define la clase Director del patrón Builder, que lee la configuración
del laberinto desde un fichero JSON y dirige la construcción.
"""
import json
from laberinto_builder import LaberintoBuilder
from laberinto_builder_rombo import LaberintoBuilderRombo


class Director:
    """
    Director es el director del patrón Builder.
    Lee la configuración del laberinto desde un fichero JSON
    y dirige la construcción usando el builder correspondiente.
    """

    def __init__(self):
        self.builder = None
        self.data_dict = {}

    def fabricar_bichos(self):
        """Construye todos los bichos definidos en la configuración."""
        bichos = self.data_dict.get('bichos', [])
        for each in bichos:
            self.builder.fabricar_bicho_modo(each.get('modo'), each.get('posicion'))

    def fabricar_juego(self):
        """Delega la creación del juego al builder."""
        self.builder.fabricar_juego()

    def fabricar_laberinto(self):
        """Construye el laberinto completo a partir de la configuración."""
        self.builder.fabricar_laberinto()

        lab_nodes = self.data_dict.get('laberinto', [])
        for each in lab_nodes:
            self.fabricar_laberinto_recursivo(each, None)

        puertas = self.data_dict.get('puertas', [])
        for pt_data in puertas:
            if len(pt_data) >= 4:
                self.builder.fabricar_puerta_lado1_or1_lado2_or2(
                    pt_data[0], pt_data[1], pt_data[2], pt_data[3]
                )

    def fabricar_laberinto_recursivo(self, un_dic, padre):
        """Construye recursivamente un nodo del laberinto y sus hijos."""
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
        """Inicializa el builder adecuado según la forma indicada en la configuración."""
        forma_val = self.data_dict.get('forma')
        if forma_val == 'poligono4':
            self.builder = LaberintoBuilder()
        elif forma_val == 'rombo':
            self.builder = LaberintoBuilderRombo()

    def leer_archivo(self, un_archivo):
        """Lee y parsea el fichero JSON de configuración del laberinto."""
        with open(un_archivo, 'r', encoding='utf-8') as file:
            self.data_dict = json.load(file)

    def obtener_juego(self):
        """Devuelve el juego construido por el builder."""
        return self.builder.juego if self.builder else None

    def procesar(self, un_archivo):
        """Proceso completo: leer, inicializar builder, construir laberinto, juego y bichos."""
        self.leer_archivo(un_archivo)
        self.ini_builder()
        self.fabricar_laberinto()
        self.fabricar_juego()
        self.fabricar_bichos()
