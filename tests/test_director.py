"""
Tests para el Director del patron Builder.

Cubre:
- Lectura de archivo JSON
- Inicializacion del builder correcto
- Proceso completo de construccion
- Manejo de errores (archivo no encontrado, forma desconocida)
"""
import unittest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from director import Director, ArchivoConfigError
from laberinto_builder import LaberintoBuilder


class TestDirectorLeerArchivo(unittest.TestCase):
    """Tests de lectura de configuracion."""

    def test_leer_archivo_json(self):
        """Lee correctamente el laberinto.json del proyecto."""
        director = Director()
        ruta = os.path.join(os.path.dirname(__file__), '..', 'laberinto.json')
        director.leer_archivo(ruta)
        self.assertIn('forma', director.data_dict)
        self.assertIn('laberinto', director.data_dict)

    def test_archivo_no_encontrado(self):
        """Lanza ArchivoConfigError si el archivo no existe."""
        director = Director()
        with self.assertRaises(ArchivoConfigError):
            director.leer_archivo('no_existe.json')

    def test_json_invalido(self):
        """Lanza ArchivoConfigError si el JSON es invalido."""
        director = Director()
        # Crear archivo temporal con JSON invalido
        ruta_tmp = os.path.join(os.path.dirname(__file__), 'tmp_invalid.json')
        try:
            with open(ruta_tmp, 'w', encoding='utf-8') as f:
                f.write('{esto no es json valido}')
            with self.assertRaises(ArchivoConfigError):
                director.leer_archivo(ruta_tmp)
        finally:
            if os.path.exists(ruta_tmp):
                os.remove(ruta_tmp)


class TestDirectorIniBuilder(unittest.TestCase):
    """Tests de inicializacion del builder."""

    def test_ini_builder_poligono4(self):
        """Con forma 'poligono4' crea un LaberintoBuilder."""
        director = Director()
        director.data_dict = {'forma': 'poligono4'}
        director.ini_builder()
        self.assertIsInstance(director.builder, LaberintoBuilder)

    def test_forma_desconocida(self):
        """Lanza ArchivoConfigError si la forma es invalida."""
        director = Director()
        director.data_dict = {'forma': 'triangulo'}
        with self.assertRaises(ArchivoConfigError):
            director.ini_builder()


class TestDirectorProcesar(unittest.TestCase):
    """Tests del proceso completo de construccion."""

    def test_procesar_completo(self):
        """procesar() crea juego con laberinto, bichos, etc."""
        director = Director()
        ruta = os.path.join(os.path.dirname(__file__), '..', 'laberinto.json')
        director.procesar(ruta)

        juego = director.obtener_juego()
        self.assertIsNotNone(juego)
        self.assertIsNotNone(juego.laberinto)

    def test_procesar_crea_habitaciones(self):
        """Tras procesar, existen las habitaciones del JSON."""
        director = Director()
        ruta = os.path.join(os.path.dirname(__file__), '..', 'laberinto.json')
        director.procesar(ruta)

        juego = director.obtener_juego()
        # El JSON tiene habitaciones 1-6
        self.assertIsNotNone(juego.obtener_habitacion(1))
        self.assertIsNotNone(juego.obtener_habitacion(2))

    def test_procesar_crea_bichos(self):
        """Tras procesar, el juego tiene bichos."""
        director = Director()
        ruta = os.path.join(os.path.dirname(__file__), '..', 'laberinto.json')
        director.procesar(ruta)

        juego = director.obtener_juego()
        # El JSON tiene 2 bichos
        self.assertEqual(len(juego.bichos), 2)

    def test_procesar_hab_salida(self):
        """Tras procesar, la habitacion 5 es de salida."""
        director = Director()
        ruta = os.path.join(os.path.dirname(__file__), '..', 'laberinto.json')
        director.procesar(ruta)

        juego = director.obtener_juego()
        hab5 = juego.obtener_habitacion(5)
        self.assertTrue(hab5.es_salida())

    def test_procesar_timer_global(self):
        """Tras procesar, el juego tiene timer_global asignado."""
        director = Director()
        ruta = os.path.join(os.path.dirname(__file__), '..', 'laberinto.json')
        director.procesar(ruta)

        juego = director.obtener_juego()
        self.assertEqual(juego.timer_global, 300)

    def test_obtener_juego_sin_builder(self):
        """Si no hay builder, obtener_juego devuelve None."""
        director = Director()
        self.assertIsNone(director.obtener_juego())


class TestDirectorJSON(unittest.TestCase):
    """Tests con JSON personalizado minimo."""

    def test_procesar_json_minimo(self):
        """Procesa un JSON minimo con solo 1 habitacion."""
        ruta_tmp = os.path.join(os.path.dirname(__file__), 'tmp_min.json')
        data = {
            "forma": "poligono4",
            "laberinto": [{"tipo": "habitacion", "num": 1}],
            "puertas": [],
            "bichos": [],
            "bombas": [],
            "nieblas": [],
            "mimicos": [],
            "temporizadores": []
        }
        try:
            with open(ruta_tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f)

            director = Director()
            director.procesar(ruta_tmp)
            juego = director.obtener_juego()

            self.assertIsNotNone(juego)
            self.assertIsNotNone(juego.obtener_habitacion(1))
            self.assertEqual(len(juego.bichos), 0)
        finally:
            if os.path.exists(ruta_tmp):
                os.remove(ruta_tmp)


if __name__ == '__main__':
    unittest.main()
