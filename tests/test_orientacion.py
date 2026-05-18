"""
Tests para las Orientaciones y el patrón Singleton.

Cubre:
- Singleton: Norte.default() siempre devuelve la misma instancia
- Cada orientación es un Singleton distinto
- caminar mueve al bicho al elemento correcto
- poner_elemento_en_contenedor asigna en el lado correcto
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from cuadrado import Cuadrado
from habitacion import Habitacion
from pared import Pared
from personaje import Personaje


class TestSingleton(unittest.TestCase):
    """Tests del patrón Singleton en orientaciones."""

    def test_norte_singleton(self):
        """Norte.default() siempre devuelve la misma instancia."""
        n1 = Norte.default()
        n2 = Norte.default()
        self.assertIs(n1, n2)

    def test_sur_singleton(self):
        """Sur.default() siempre devuelve la misma instancia."""
        s1 = Sur.default()
        s2 = Sur.default()
        self.assertIs(s1, s2)

    def test_este_singleton(self):
        """Este.default() siempre devuelve la misma instancia."""
        e1 = Este.default()
        e2 = Este.default()
        self.assertIs(e1, e2)

    def test_oeste_singleton(self):
        """Oeste.default() siempre devuelve la misma instancia."""
        o1 = Oeste.default()
        o2 = Oeste.default()
        self.assertIs(o1, o2)

    def test_norte_no_es_sur(self):
        """Norte y Sur son Singletons diferentes."""
        self.assertIsNot(Norte.default(), Sur.default())

    def test_este_no_es_oeste(self):
        """Este y Oeste son Singletons diferentes."""
        self.assertIsNot(Este.default(), Oeste.default())


class TestNortePoner(unittest.TestCase):
    """Tests de poner_elemento_en_contenedor de Norte."""

    def test_norte_poner_pared(self):
        """Norte.poner_elemento_en_contenedor pone la pared en cuad.norte."""
        cuad = Cuadrado()
        pared = Pared()
        norte = Norte.default()

        norte.poner_elemento_en_contenedor(pared, cuad)

        self.assertEqual(cuad.norte, pared)


class TestSurPoner(unittest.TestCase):
    """Tests de poner_elemento_en_contenedor de Sur."""

    def test_sur_poner_pared(self):
        """Sur.poner_elemento_en_contenedor pone la pared en cuad.sur."""
        cuad = Cuadrado()
        pared = Pared()
        sur = Sur.default()

        sur.poner_elemento_en_contenedor(pared, cuad)

        self.assertEqual(cuad.sur, pared)


class TestEstePoner(unittest.TestCase):
    """Tests de poner_elemento_en_contenedor de Este."""

    def test_este_poner_pared(self):
        """Este.poner_elemento_en_contenedor pone la pared en cuad.este."""
        cuad = Cuadrado()
        pared = Pared()
        este = Este.default()

        este.poner_elemento_en_contenedor(pared, cuad)

        self.assertEqual(cuad.este, pared)


class TestOestePoner(unittest.TestCase):
    """Tests de poner_elemento_en_contenedor de Oeste."""

    def test_oeste_poner_pared(self):
        """Oeste.poner_elemento_en_contenedor pone la pared en cuad.oeste."""
        cuad = Cuadrado()
        pared = Pared()
        oeste = Oeste.default()

        oeste.poner_elemento_en_contenedor(pared, cuad)

        self.assertEqual(cuad.oeste, pared)


class TestNorteCaminar(unittest.TestCase):
    """Tests de caminar con orientaciones."""

    def test_norte_caminar_pared(self):
        """Al caminar al norte hacia una pared, se queda en la misma hab."""
        hab = Habitacion()
        hab.num = 1
        hab.forma = Cuadrado()
        pared = Pared()
        hab.forma.norte = pared

        pj = Personaje()
        pj.posicion = hab

        norte = Norte.default()
        norte.caminar(pj)

        # Al chocar con pared, la posición no cambia a otra habitación
        self.assertEqual(pj.posicion, hab)


if __name__ == '__main__':
    unittest.main()
