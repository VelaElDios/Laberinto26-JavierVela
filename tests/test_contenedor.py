"""
Tests para Contenedor, Habitacion y Laberinto.

Cubre:
- Patrón Composite (agregar/eliminar hijos)
- Entrar en habitación cambia posición
- Laberinto agregar/obtener habitaciones
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contenedor import Contenedor
from habitacion import Habitacion
from laberinto import Laberinto
from personaje import Personaje
from pared import Pared


class TestContenedor(unittest.TestCase):
    """Tests del patrón Composite — Contenedor."""

    def test_agregar_hijo(self):
        """agregar_hijo añade a la lista de hijos."""
        cont = Contenedor()
        pared = Pared()
        cont.agregar_hijo(pared)

        self.assertIn(pared, cont.hijos)

    def test_agregar_varios_hijos(self):
        """Se pueden añadir múltiples hijos."""
        cont = Contenedor()
        p1 = Pared()
        p2 = Pared()
        cont.agregar_hijo(p1)
        cont.agregar_hijo(p2)

        self.assertEqual(len(cont.hijos), 2)

    def test_eliminar_hijo(self):
        """eliminar_hijo quita un hijo de la lista."""
        cont = Contenedor()
        pared = Pared()
        cont.agregar_hijo(pared)
        cont.eliminar_hijo(pared)

        self.assertNotIn(pared, cont.hijos)

    def test_eliminar_hijo_inexistente(self):
        """Eliminar un hijo que no está no lanza excepción."""
        cont = Contenedor()
        pared = Pared()
        # No debería lanzar error
        cont.eliminar_hijo(pared)
        self.assertEqual(len(cont.hijos), 0)

    def test_hijos_inicia_vacio(self):
        """Un contenedor nuevo tiene la lista de hijos vacía."""
        cont = Contenedor()
        self.assertEqual(cont.hijos, [])


class TestHabitacion(unittest.TestCase):
    """Tests de Habitación."""

    def test_entrar_cambia_posicion(self):
        """Al entrar en una habitación, alguien.posicion apunta a ella."""
        hab = Habitacion()
        hab.num = 5
        pj = Personaje()

        hab.entrar(pj)

        self.assertEqual(pj.posicion, hab)

    def test_entrar_actualiza_evento(self):
        """Al entrar, se actualiza ultimo_evento del personaje."""
        hab = Habitacion()
        hab.num = 1
        pj = Personaje()

        hab.entrar(pj)

        self.assertNotEqual(pj.ultimo_evento, "")

    def test_str_habitacion(self):
        """La representación string es 'Hab-X'."""
        hab = Habitacion()
        hab.num = 3
        self.assertEqual(str(hab), "Hab-3")

    def test_habitacion_es_contenedor(self):
        """Habitacion hereda de Contenedor (patrón Composite)."""
        hab = Habitacion()
        self.assertIsInstance(hab, Contenedor)

    def test_habitacion_puede_tener_hijos(self):
        """Una habitación puede contener elementos hijos."""
        hab = Habitacion()
        hab.num = 1
        pared = Pared()
        hab.agregar_hijo(pared)

        self.assertIn(pared, hab.hijos)


class TestLaberinto(unittest.TestCase):
    """Tests de Laberinto."""

    def test_agregar_y_obtener_habitacion(self):
        """Puedes agregar una habitación y recuperarla por número."""
        lab = Laberinto()
        hab = Habitacion()
        hab.num = 1
        lab.agregar_habitacion(hab)

        resultado = lab.obtener_habitacion(1)
        self.assertEqual(resultado, hab)

    def test_obtener_habitacion_inexistente(self):
        """Si pides una habitación que no existe, devuelve None."""
        lab = Laberinto()
        resultado = lab.obtener_habitacion(99)
        self.assertIsNone(resultado)

    def test_agregar_multiples_habitaciones(self):
        """Puedes agregar y obtener varias habitaciones."""
        lab = Laberinto()
        hab1 = Habitacion()
        hab1.num = 1
        hab2 = Habitacion()
        hab2.num = 2

        lab.agregar_habitacion(hab1)
        lab.agregar_habitacion(hab2)

        self.assertEqual(lab.obtener_habitacion(1), hab1)
        self.assertEqual(lab.obtener_habitacion(2), hab2)

    def test_laberinto_entrar_va_a_hab1(self):
        """Entrar en el laberinto coloca al personaje en la habitación 1."""
        lab = Laberinto()
        hab1 = Habitacion()
        hab1.num = 1
        lab.agregar_habitacion(hab1)

        pj = Personaje()
        lab.entrar(pj)

        self.assertEqual(pj.posicion, hab1)

    def test_laberinto_es_contenedor(self):
        """Laberinto hereda de Contenedor (patrón Composite)."""
        lab = Laberinto()
        self.assertIsInstance(lab, Contenedor)


if __name__ == '__main__':
    unittest.main()
