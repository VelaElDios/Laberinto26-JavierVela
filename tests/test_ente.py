"""
Tests para Ente, Personaje y Bicho.

Cubre:
- Vidas iniciales del personaje
- Mecánica de combate (es_atacado_por)
- Condición de muerte (vidas <= 0)
- esta_vivo()
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ente import Ente
from personaje import Personaje
from bicho import Bicho
from agresivo import Agresivo
from habitacion import Habitacion
from juego import Juego


class TestPersonaje(unittest.TestCase):
    """Tests del Personaje."""

    def test_vidas_iniciales(self):
        """El personaje empieza con 3 vidas."""
        pj = Personaje()
        self.assertEqual(pj.vidas, 3)

    def test_poder_inicial(self):
        """El personaje empieza con poder 1."""
        pj = Personaje()
        self.assertEqual(pj.poder, 1)

    def test_posicion_inicial_none(self):
        """El personaje empieza sin posición."""
        pj = Personaje()
        self.assertIsNone(pj.posicion)

    def test_nombre_inicial_vacio(self):
        """El personaje empieza sin nombre."""
        pj = Personaje()
        self.assertEqual(pj.nombre, "")

    def test_clase_inicial_alumno(self):
        """El personaje empieza como alumno."""
        pj = Personaje()
        self.assertEqual(pj.clase, "alumno")

    def test_dificultad_inicial_normal(self):
        """La dificultad empieza en normal."""
        pj = Personaje()
        self.assertEqual(pj.dificultad, "normal")

    def test_str_devuelve_nombre(self):
        """str(personaje) devuelve el nombre."""
        pj = Personaje()
        pj.nombre = "TestHero"
        self.assertEqual(str(pj), "TestHero")

    def test_buscar_enemigo_devuelve_none(self):
        """El personaje no busca enemigos activamente."""
        pj = Personaje()
        self.assertIsNone(pj.buscar_enemigo())


class TestCombate(unittest.TestCase):
    """Tests de la mecánica de combate entre entes."""

    def test_es_atacado_pierde_vidas(self):
        """Al ser atacado, el ente pierde vidas según el poder del atacante."""
        pj = Personaje()
        pj.vidas = 10

        atacante = Personaje()
        atacante.poder = 3

        pj.es_atacado_por(atacante)

        self.assertEqual(pj.vidas, 7)

    def test_es_atacado_varias_veces(self):
        """Múltiples ataques van reduciendo vidas."""
        pj = Personaje()
        pj.vidas = 10

        atacante = Personaje()
        atacante.poder = 2

        pj.es_atacado_por(atacante)
        pj.es_atacado_por(atacante)

        self.assertEqual(pj.vidas, 6)

    def test_esta_vivo_true(self):
        """esta_vivo devuelve True si vidas > 0."""
        pj = Personaje()
        pj.vidas = 5
        self.assertTrue(pj.esta_vivo())

    def test_esta_vivo_false(self):
        """esta_vivo devuelve False si vidas <= 0."""
        pj = Personaje()
        pj.vidas = 0
        self.assertFalse(pj.esta_vivo())

    def test_muere_al_llegar_a_0_vidas(self):
        """Cuando las vidas llegan a 0, se llama muero()."""
        juego = Juego()
        juego.fabricar_lab2_hab()
        juego.agregar_personaje("Test")

        pj = juego.person
        pj.vidas = 1

        atacante = Personaje()
        atacante.poder = 1

        pj.es_atacado_por(atacante)

        # El juego debe estar finalizado con derrota
        self.assertTrue(juego.finalizado)
        self.assertEqual(juego.resultado, "derrota")


class TestBichoEnte(unittest.TestCase):
    """Tests del Bicho como Ente."""

    def test_bicho_vidas_iniciales(self):
        """Un bicho nuevo tiene 50 vidas (hereda de Ente)."""
        bicho = Bicho()
        self.assertEqual(bicho.vidas, 50)

    def test_bicho_esta_vivo(self):
        """Un bicho nuevo está vivo."""
        bicho = Bicho()
        self.assertTrue(bicho.esta_vivo())

    def test_bicho_muere(self):
        """Al matar un bicho, se notifica al juego."""
        juego = Juego()
        juego.fabricar_lab2_hab()

        bicho = Bicho()
        bicho.modo = Agresivo()
        bicho.juego = juego
        hab = juego.obtener_habitacion(1)
        hab.entrar(bicho)
        juego.agregar_bicho(bicho)

        bicho.vidas = 1
        atacante = Personaje()
        atacante.poder = 1
        bicho.es_atacado_por(atacante)

        # El bicho debe tener 0 vidas
        self.assertEqual(bicho.vidas, 0)
        self.assertFalse(bicho.esta_vivo())

    def test_bicho_buscar_enemigo_sin_juego(self):
        """Sin juego asignado, buscar_enemigo devuelve None."""
        bicho = Bicho()
        self.assertIsNone(bicho.buscar_enemigo())


if __name__ == '__main__':
    unittest.main()
