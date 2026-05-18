"""
Tests para Forma y Cuadrado.

Cubre:
- Patrón Bridge (Forma desacopla Contenedor de geometría)
- Cuadrado tiene 4 orientaciones (norte, sur, este, oeste)
- poner_en_elemento delega a la orientación
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forma import Forma
from cuadrado import Cuadrado
from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from pared import Pared


class TestForma(unittest.TestCase):
    """Tests de Forma — patrón Bridge."""

    def test_orientaciones_inicia_vacia(self):
        """Una forma nueva no tiene orientaciones."""
        forma = Forma()
        self.assertEqual(forma.orientaciones, [])

    def test_agregar_orientacion(self):
        """agregar_orientacion añade a la lista."""
        forma = Forma()
        norte = Norte.default()
        forma.agregar_orientacion(norte)

        self.assertIn(norte, forma.orientaciones)

    def test_eliminar_orientacion(self):
        """eliminar_orientacion quita de la lista."""
        forma = Forma()
        norte = Norte.default()
        forma.agregar_orientacion(norte)
        forma.eliminar_orientacion(norte)

        self.assertNotIn(norte, forma.orientaciones)

    def test_obtener_orientacion_aleatoria_vacia(self):
        """Si no hay orientaciones, devuelve None."""
        forma = Forma()
        self.assertIsNone(forma.obtener_orientacion_aleatoria())

    def test_obtener_orientacion_aleatoria(self):
        """Devuelve una orientación válida de las disponibles."""
        forma = Forma()
        norte = Norte.default()
        forma.agregar_orientacion(norte)

        resultado = forma.obtener_orientacion_aleatoria()
        self.assertEqual(resultado, norte)

    def test_poner_en_elemento(self):
        """poner_en_elemento delega a la orientación para colocar el elemento."""
        cuad = Cuadrado()
        norte = Norte.default()
        cuad.agregar_orientacion(norte)
        pared = Pared()

        cuad.poner_en_elemento(norte, pared)

        self.assertEqual(cuad.norte, pared)


class TestCuadrado(unittest.TestCase):
    """Tests de Cuadrado — implementación concreta de Forma."""

    def test_cuadrado_atributos_none_por_defecto(self):
        """Un cuadrado nuevo tiene norte, sur, este, oeste a None."""
        cuad = Cuadrado()
        self.assertIsNone(cuad.norte)
        self.assertIsNone(cuad.sur)
        self.assertIsNone(cuad.este)
        self.assertIsNone(cuad.oeste)

    def test_cuadrado_hereda_de_forma(self):
        """Cuadrado hereda de Forma (patrón Bridge)."""
        cuad = Cuadrado()
        self.assertIsInstance(cuad, Forma)

    def test_cuadrado_poner_en_4_lados(self):
        """Se pueden poner elementos en los 4 lados del cuadrado."""
        cuad = Cuadrado()
        p_norte = Pared()
        p_sur = Pared()
        p_este = Pared()
        p_oeste = Pared()

        norte = Norte.default()
        sur = Sur.default()
        este = Este.default()
        oeste = Oeste.default()

        cuad.poner_en_elemento(norte, p_norte)
        cuad.poner_en_elemento(sur, p_sur)
        cuad.poner_en_elemento(este, p_este)
        cuad.poner_en_elemento(oeste, p_oeste)

        self.assertEqual(cuad.norte, p_norte)
        self.assertEqual(cuad.sur, p_sur)
        self.assertEqual(cuad.este, p_este)
        self.assertEqual(cuad.oeste, p_oeste)


if __name__ == '__main__':
    unittest.main()
