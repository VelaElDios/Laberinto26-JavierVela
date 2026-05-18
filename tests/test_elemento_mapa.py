"""
Tests para los elementos hoja del mapa: Pared y Puerta.

Cubre:
- Pared bloquea el paso
- Puerta abierta/cerrada
- Métodos de tipo (es_puerta, es_bomba, etc.)
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pared import Pared
from puerta import Puerta
from habitacion import Habitacion
from personaje import Personaje


class TestPared(unittest.TestCase):
    """Tests de la clase Pared."""

    def test_pared_no_cambia_posicion(self):
        """Al chocar con una pared, el personaje NO cambia de posición."""
        hab = Habitacion()
        hab.num = 1
        pj = Personaje()
        pj.posicion = hab

        pared = Pared()
        pared.entrar(pj)

        # La posición sigue siendo la misma habitación
        self.assertEqual(pj.posicion, hab)

    def test_pared_informa_choque(self):
        """Al chocar con la pared, se actualiza ultimo_evento."""
        pj = Personaje()
        pared = Pared()
        pared.entrar(pj)

        self.assertIn("pared", pj.ultimo_evento.lower())

    def test_pared_es_puerta_false(self):
        """Una pared NO es una puerta."""
        pared = Pared()
        self.assertFalse(pared.es_puerta())

    def test_pared_es_bomba_false(self):
        """Una pared NO es una bomba."""
        pared = Pared()
        self.assertFalse(pared.es_bomba())

    def test_pared_es_salida_false(self):
        """Una pared NO es una salida."""
        pared = Pared()
        self.assertFalse(pared.es_salida())

    def test_pared_str(self):
        """La representación string de una pared es 'Pared'."""
        pared = Pared()
        self.assertEqual(str(pared), "Pared")


class TestPuerta(unittest.TestCase):
    """Tests de la clase Puerta."""

    def setUp(self):
        """Prepara dos habitaciones conectadas por una puerta."""
        self.hab1 = Habitacion()
        self.hab1.num = 1
        self.hab2 = Habitacion()
        self.hab2.num = 2
        self.puerta = Puerta()
        self.puerta.lado1 = self.hab1
        self.puerta.lado2 = self.hab2
        self.pj = Personaje()

    def test_puerta_cerrada_no_deja_pasar(self):
        """Si la puerta está cerrada, el personaje no pasa."""
        self.pj.posicion = self.hab1
        self.puerta.entrar(self.pj)

        # Sigue en la misma habitación
        self.assertEqual(self.pj.posicion, self.hab1)

    def test_puerta_abierta_pasa_lado1_a_lado2(self):
        """Si la puerta está abierta y estamos en lado1, pasamos a lado2."""
        self.pj.posicion = self.hab1
        self.puerta.abrir()
        self.puerta.entrar(self.pj)

        self.assertEqual(self.pj.posicion, self.hab2)

    def test_puerta_abierta_pasa_lado2_a_lado1(self):
        """Si la puerta está abierta y estamos en lado2, pasamos a lado1."""
        self.pj.posicion = self.hab2
        self.puerta.abrir()
        self.puerta.entrar(self.pj)

        self.assertEqual(self.pj.posicion, self.hab1)

    def test_puerta_abrir(self):
        """abrir() pone la puerta como abierta."""
        self.puerta.abrir()
        self.assertTrue(self.puerta.abierta)

    def test_puerta_cerrar(self):
        """cerrar() pone la puerta como cerrada."""
        self.puerta.abrir()
        self.puerta.cerrar()
        self.assertFalse(self.puerta.abierta)

    def test_puerta_cerrada_informa(self):
        """Al intentar pasar por puerta cerrada, se avisa al personaje."""
        self.pj.posicion = self.hab1
        self.puerta.entrar(self.pj)

        self.assertIn("cerrada", self.pj.ultimo_evento.lower())

    def test_puerta_es_puerta_true(self):
        """Una puerta ES una puerta."""
        self.assertTrue(self.puerta.es_puerta())

    def test_puerta_es_bomba_false(self):
        """Una puerta NO es una bomba."""
        self.assertFalse(self.puerta.es_bomba())

    def test_puerta_str(self):
        """La representación string muestra los números de habitaciones."""
        self.assertIn("1", str(self.puerta))
        self.assertIn("2", str(self.puerta))

    def test_puerta_inicia_cerrada(self):
        """Una puerta nueva está cerrada por defecto."""
        puerta_nueva = Puerta()
        self.assertFalse(puerta_nueva.abierta)


if __name__ == '__main__':
    unittest.main()
