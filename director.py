"""
Módulo director.

Define la clase Director del patrón Builder, que lee la configuración
del laberinto desde un fichero JSON y dirige la construcción.
"""
import json
from laberinto_builder import LaberintoBuilder
from laberinto_builder_rombo import LaberintoBuilderRombo


class DirectorError(Exception):
    """Excepción base para errores del Director."""


class ArchivoConfigError(DirectorError):
    """Error al leer o parsear el archivo de configuración."""


class BuilderNoInicializadoError(DirectorError):
    """El builder no se ha inicializado correctamente."""


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
        if not self.builder:
            raise BuilderNoInicializadoError("Builder no inicializado al fabricar bichos.")
        bichos = self.data_dict.get('bichos', [])
        for each in bichos:
            try:
                self.builder.fabricar_bicho_modo(each.get('modo'), each.get('posicion'))
            except (AttributeError, TypeError) as exc:
                print(f"Error al crear bicho {each}: {exc}")

    def fabricar_bombas(self):
        """Construye todas las bombas definidas en la configuración."""
        if not self.builder:
            raise BuilderNoInicializadoError("Builder no inicializado al fabricar bombas.")
        bombas = self.data_dict.get('bombas', [])
        for num_hab in bombas:
            try:
                self.builder.fabricar_bomba_en_habitacion(num_hab)
            except (AttributeError, TypeError) as exc:
                print(f"Error al crear bomba en hab {num_hab}: {exc}")

    def fabricar_nieblas(self):
        """Coloca niebla en las habitaciones indicadas en la config."""
        if not self.builder:
            raise BuilderNoInicializadoError(
                "Builder no inicializado al fabricar nieblas."
            )
        nieblas = self.data_dict.get('nieblas', [])
        for num_hab in nieblas:
            try:
                self.builder.fabricar_niebla_en_habitacion(num_hab)
            except (AttributeError, TypeError) as exc:
                print(
                    f"Error al crear niebla en hab {num_hab}: {exc}"
                )

    def fabricar_mimicos(self):
        """Coloca mimicos en las habitaciones indicadas en la config."""
        if not self.builder:
            raise BuilderNoInicializadoError(
                "Builder no inicializado al fabricar mimicos."
            )
        mimicos = self.data_dict.get('mimicos', [])
        for num_hab in mimicos:
            try:
                self.builder.fabricar_mimico_en_habitacion(num_hab)
            except (AttributeError, TypeError) as exc:
                print(
                    f"Error al crear mimico en hab {num_hab}: {exc}"
                )

    def fabricar_juego(self):
        """Delega la creación del juego al builder."""
        if not self.builder:
            raise BuilderNoInicializadoError("Builder no inicializado al fabricar juego.")
        self.builder.fabricar_juego()

    def fabricar_laberinto(self):
        """Construye el laberinto completo a partir de la configuración."""
        if not self.builder:
            raise BuilderNoInicializadoError("Builder no inicializado al fabricar laberinto.")
        self.builder.fabricar_laberinto()

        lab_nodes = self.data_dict.get('laberinto', [])
        for each in lab_nodes:
            self.fabricar_laberinto_recursivo(each, None)

        puertas = self.data_dict.get('puertas', [])
        for pt_data in puertas:
            if len(pt_data) >= 4:
                try:
                    self.builder.fabricar_puerta_lado1_or1_lado2_or2(
                        pt_data[0], pt_data[1], pt_data[2], pt_data[3]
                    )
                except (AttributeError, TypeError) as exc:
                    print(f"Error al crear puerta {pt_data}: {exc}")

    def fabricar_laberinto_recursivo(self, un_dic, padre):
        """Construye recursivamente un nodo del laberinto y sus hijos."""
        tipo = un_dic.get('tipo', '')
        num = un_dic.get('num')
        con = None

        try:
            if tipo == 'habitacion':
                con = self.builder.fabricar_habitacion(num)
            elif tipo == 'habitacion_salida':
                con = self.builder.fabricar_habitacion_salida(num)
            elif tipo == 'habitacion_tienda':
                con = self.builder.fabricar_habitacion_tienda(num)
            elif tipo == 'armario':
                con = self.builder.fabricar_armario(num, padre)
            elif tipo == 'bomba':
                con = self.builder.fabricar_bomba_en(padre)
            else:
                print(f"Tipo de nodo desconocido: '{tipo}'")
        except (AttributeError, TypeError) as exc:
            print(f"Error al fabricar nodo tipo '{tipo}' num {num}: {exc}")

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
        else:
            raise ArchivoConfigError(
                f"Forma desconocida en configuración: '{forma_val}'"
            )

    def leer_archivo(self, un_archivo):
        """Lee y parsea el fichero JSON de configuración del laberinto."""
        try:
            with open(un_archivo, 'r', encoding='utf-8') as file:
                self.data_dict = json.load(file)
        except FileNotFoundError as exc:
            raise ArchivoConfigError(f"Archivo no encontrado: {un_archivo}") from exc
        except json.JSONDecodeError as exc:
            raise ArchivoConfigError(f"JSON inválido en {un_archivo}: {exc}") from exc

    def obtener_juego(self):
        """Devuelve el juego construido por el builder."""
        return self.builder.juego if self.builder else None

    def fabricar_temporizadores(self):
        """Coloca temporizadores en las habitaciones de la config."""
        if not self.builder:
            raise BuilderNoInicializadoError(
                "Builder no inicializado al fabricar temporizadores."
            )
        temps = self.data_dict.get('temporizadores', [])
        for item in temps:
            try:
                num_hab = item.get('habitacion')
                segs = item.get('segundos', 60)
                self.builder.fabricar_temporizador_en_habitacion(
                    num_hab, segs
                )
            except (AttributeError, TypeError) as exc:
                print(
                    f"Error al crear temporizador: {exc}"
                )

    def procesar(self, un_archivo):
        """Proceso completo: leer, inicializar builder, construir
        laberinto, juego, bombas, nieblas, mimicos, temporizadores
        y bichos."""
        self.leer_archivo(un_archivo)
        self.ini_builder()
        self.fabricar_laberinto()
        self.fabricar_juego()
        self.fabricar_bombas()
        self.fabricar_nieblas()
        self.fabricar_mimicos()
        self.fabricar_temporizadores()
        self.fabricar_bichos()
        # Timer global del laberinto
        timer_global = self.data_dict.get('timer_global')
        if timer_global and self.builder.juego:
            self.builder.juego.timer_global = timer_global
