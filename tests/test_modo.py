"""
Tests para Modo, Agresivo y Perezoso.

Cubre:
- Patrón State: los bichos delegan su comportamiento al modo
- Agresivo.es_agresivo() devuelve True
- Perezoso.es_perezoso() devuelve True
- Bicho delega al modo correctamente
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modo import Modo
from agresivo import Agresivo
from perezoso import Perezoso
from bicho import Bicho


class TestAgresivo(unittest.TestCase):
    """Tests del modo Agresivo — patrón State."""

    def test_es_agresivo(self):
        """Agresivo.es_agresivo() devuelve True."""
        agr = Agresivo()
        self.assertTrue(agr.es_agresivo())

    def test_no_es_perezoso(self):
        """Agresivo.es_perezoso() devuelve False."""
        agr = Agresivo()
        self.assertFalse(agr.es_perezoso())

    def test_str(self):
        """La representación string del modo Agresivo."""
        agr = Agresivo()
        self.assertEqual(str(agr), "Agresivo")


class TestPerezoso(unittest.TestCase):
    """Tests del modo Perezoso — patrón State."""

    def test_es_perezoso(self):
        """Perezoso.es_perezoso() devuelve True."""
        per = Perezoso()
        self.assertTrue(per.es_perezoso())

    def test_no_es_agresivo(self):
        """Perezoso.es_agresivo() devuelve False."""
        per = Perezoso()
        self.assertFalse(per.es_agresivo())

    def test_str(self):
        """La representación string del modo Perezoso."""
        per = Perezoso()
        self.assertEqual(str(per), "Perezoso")


class TestModoBase(unittest.TestCase):
    """Tests de la clase base Modo."""

    def test_modo_base_es_agresivo_false(self):
        """Modo base devuelve False para es_agresivo."""
        modo = Modo()
        self.assertFalse(modo.es_agresivo())

    def test_modo_base_es_perezoso_false(self):
        """Modo base devuelve False para es_perezoso."""
        modo = Modo()
        self.assertFalse(modo.es_perezoso())


class TestBichoDelegaModo(unittest.TestCase):
    """Tests de delegación del bicho al modo — patrón State."""

    def test_bicho_con_agresivo_es_agresivo(self):
        """Un bicho con modo Agresivo delega es_agresivo() → True."""
        bicho = Bicho()
        bicho.modo = Agresivo()

        self.assertTrue(bicho.es_agresivo())

    def test_bicho_con_perezoso_es_perezoso(self):
        """Un bicho con modo Perezoso delega es_perezoso() → True."""
        bicho = Bicho()
        bicho.modo = Perezoso()

        self.assertTrue(bicho.es_perezoso())

    def test_bicho_sin_modo_no_es_agresivo(self):
        """Un bicho sin modo devuelve False para es_agresivo."""
        bicho = Bicho()
        self.assertFalse(bicho.es_agresivo())

    def test_bicho_sin_modo_no_es_perezoso(self):
        """Un bicho sin modo devuelve False para es_perezoso."""
        bicho = Bicho()
        self.assertFalse(bicho.es_perezoso())

    def test_bicho_str_con_modo(self):
        """La representación string del bicho incluye su modo."""
        bicho = Bicho()
        bicho.modo = Agresivo()
        self.assertIn("Agresivo", str(bicho))

    def test_bicho_str_sin_modo(self):
        """Un bicho sin modo muestra 'SinModo'."""
        bicho = Bicho()
        self.assertIn("SinModo", str(bicho))


if __name__ == '__main__':
    unittest.main()
