"""
Tests para LaberintoBuilder.

Cubre el patron Builder: construccion paso a paso del laberinto.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from laberinto_builder import LaberintoBuilder
from laberinto import Laberinto
from habitacion import Habitacion
from habitacion_salida import HabitacionSalida
from juego import Juego
from cuadrado import Cuadrado
from pared import Pared
from puerta import Puerta
from bomba import Bomba


class TestBuilderInit(unittest.TestCase):
    def test_builder_sin_laberinto(self):
        builder = LaberintoBuilder()
        self.assertIsNone(builder.laberinto)

    def test_builder_sin_juego(self):
        builder = LaberintoBuilder()
        self.assertIsNone(builder.juego)


class TestBuilderLaberinto(unittest.TestCase):
    def test_fabricar_laberinto(self):
        builder = LaberintoBuilder()
        builder.fabricar_laberinto()
        self.assertIsInstance(builder.laberinto, Laberinto)


class TestBuilderHabitacion(unittest.TestCase):
    def setUp(self):
        self.builder = LaberintoBuilder()
        self.builder.fabricar_laberinto()

    def test_fabricar_habitacion(self):
        hab = self.builder.fabricar_habitacion(1)
        self.assertEqual(hab.num, 1)

    def test_habitacion_tiene_forma_cuadrada(self):
        hab = self.builder.fabricar_habitacion(1)
        self.assertIsInstance(hab.forma, Cuadrado)

    def test_habitacion_tiene_4_paredes(self):
        hab = self.builder.fabricar_habitacion(1)
        self.assertIsInstance(hab.forma.norte, Pared)
        self.assertIsInstance(hab.forma.sur, Pared)
        self.assertIsInstance(hab.forma.este, Pared)
        self.assertIsInstance(hab.forma.oeste, Pared)

    def test_habitacion_queda_en_laberinto(self):
        self.builder.fabricar_habitacion(1)
        self.assertIsNotNone(self.builder.laberinto.obtener_habitacion(1))

    def test_fabricar_habitacion_salida(self):
        hab = self.builder.fabricar_habitacion_salida(5)
        self.assertIsInstance(hab, HabitacionSalida)
        self.assertTrue(hab.es_salida())


class TestBuilderPuerta(unittest.TestCase):
    def setUp(self):
        self.builder = LaberintoBuilder()
        self.builder.fabricar_laberinto()
        self.builder.fabricar_habitacion(1)
        self.builder.fabricar_habitacion(2)

    def test_fabricar_puerta(self):
        self.builder.fabricar_puerta_lado1_or1_lado2_or2(1, "sur", 2, "norte")
        hab1 = self.builder.laberinto.obtener_habitacion(1)
        self.assertIsInstance(hab1.forma.sur, Puerta)

    def test_puerta_conecta_habitaciones(self):
        self.builder.fabricar_puerta_lado1_or1_lado2_or2(1, "sur", 2, "norte")
        hab1 = self.builder.laberinto.obtener_habitacion(1)
        hab2 = self.builder.laberinto.obtener_habitacion(2)
        puerta = hab1.forma.sur
        self.assertEqual(puerta.lado1, hab1)
        self.assertEqual(puerta.lado2, hab2)


class TestBuilderJuego(unittest.TestCase):
    def test_fabricar_juego(self):
        builder = LaberintoBuilder()
        builder.fabricar_laberinto()
        builder.fabricar_juego()
        self.assertIsInstance(builder.juego, Juego)
        self.assertEqual(builder.juego.laberinto, builder.laberinto)


class TestBuilderBicho(unittest.TestCase):
    def setUp(self):
        self.builder = LaberintoBuilder()
        self.builder.fabricar_laberinto()
        self.builder.fabricar_habitacion(1)
        self.builder.fabricar_juego()

    def test_fabricar_bicho_agresivo(self):
        self.builder.fabricar_bicho_modo("agresivo", 1)
        bicho = self.builder.juego.bichos[0]
        self.assertTrue(bicho.es_agresivo())

    def test_fabricar_bicho_perezoso(self):
        self.builder.fabricar_bicho_modo("perezoso", 1)
        bicho = self.builder.juego.bichos[0]
        self.assertTrue(bicho.es_perezoso())

    def test_bicho_tiene_juego(self):
        self.builder.fabricar_bicho_modo("agresivo", 1)
        bicho = self.builder.juego.bichos[0]
        self.assertEqual(bicho.juego, self.builder.juego)


class TestBuilderBomba(unittest.TestCase):
    def setUp(self):
        self.builder = LaberintoBuilder()
        self.builder.fabricar_laberinto()
        self.builder.fabricar_habitacion(1)

    def test_fabricar_bomba_en_habitacion(self):
        bomba = self.builder.fabricar_bomba_en_habitacion(1)
        self.assertTrue(bomba.activa)
        self.assertTrue(bomba.es_bomba())

    def test_bomba_como_hijo(self):
        self.builder.fabricar_bomba_en_habitacion(1)
        hab = self.builder.laberinto.obtener_habitacion(1)
        bombas = [h for h in hab.hijos if h.es_bomba()]
        self.assertEqual(len(bombas), 1)

    def test_bomba_en_hab_inexistente(self):
        self.assertIsNone(self.builder.fabricar_bomba_en_habitacion(99))


class TestBuilderNiebla(unittest.TestCase):
    def setUp(self):
        self.builder = LaberintoBuilder()
        self.builder.fabricar_laberinto()
        self.builder.fabricar_habitacion(1)

    def test_fabricar_niebla(self):
        niebla = self.builder.fabricar_niebla_en_habitacion(1)
        self.assertTrue(niebla.activa)

    def test_niebla_en_hab_inexistente(self):
        self.assertIsNone(self.builder.fabricar_niebla_en_habitacion(99))


if __name__ == '__main__':
    unittest.main()
