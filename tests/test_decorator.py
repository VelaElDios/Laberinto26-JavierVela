"""
Tests para Decorator y Bomba.

Cubre:
- Patrón Decorator: Bomba envuelve otro ElementoMapa
- Bomba activar/desactivar
- Bomba.es_bomba() devuelve True
- Bomba activa ejecuta comportamiento explosivo
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decorator import Decorator
from bomba import Bomba
from pared import Pared
from personaje import Personaje
from habitacion import Habitacion


class TestDecorator(unittest.TestCase):
    """Tests del patrón Decorator base."""

    def test_decorator_sin_elemento(self):
        """Un decorator nuevo tiene em=None."""
        dec = Decorator()
        self.assertIsNone(dec.em)

    def test_decorator_delega_entrar(self):
        """Si tiene un elemento decorado, delega entrar a él."""
        dec = Decorator()
        hab = Habitacion()
        hab.num = 1
        dec.em = hab

        pj = Personaje()
        dec.entrar(pj)

        # Delega al elemento decorado (la habitación)
        self.assertEqual(pj.posicion, hab)

    def test_decorator_sin_em_no_falla(self):
        """Si no tiene elemento decorado, entrar no lanza excepción."""
        dec = Decorator()
        pj = Personaje()
        # No debería lanzar error
        dec.entrar(pj)


class TestBomba(unittest.TestCase):
    """Tests de Bomba — Decorator concreto."""

    def test_bomba_es_bomba(self):
        """Bomba.es_bomba() devuelve True."""
        bomba = Bomba()
        self.assertTrue(bomba.es_bomba())

    def test_bomba_no_es_puerta(self):
        """Bomba.es_puerta() devuelve False."""
        bomba = Bomba()
        self.assertFalse(bomba.es_puerta())

    def test_bomba_inicia_desactivada(self):
        """Una bomba nueva está desactivada por defecto."""
        bomba = Bomba()
        self.assertFalse(bomba.activa)

    def test_bomba_activar(self):
        """activar() pone la bomba activa."""
        bomba = Bomba()
        bomba.activar()
        self.assertTrue(bomba.activa)

    def test_bomba_desactivar(self):
        """desactivar() pone la bomba inactiva."""
        bomba = Bomba()
        bomba.activar()
        bomba.desactivar()
        self.assertFalse(bomba.activa)

    def test_bomba_activa_no_lanza_error(self):
        """Al entrar con bomba activa, no lanza excepción."""
        bomba = Bomba()
        bomba.activar()
        pj = Personaje()

        # No debería lanzar error
        bomba.entrar(pj)

    def test_bomba_hereda_de_decorator(self):
        """Bomba hereda de Decorator (patrón Decorator)."""
        bomba = Bomba()
        self.assertIsInstance(bomba, Decorator)


if __name__ == '__main__':
    unittest.main()
