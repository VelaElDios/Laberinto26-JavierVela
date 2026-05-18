"""
Tests para la clase Juego.

Cubre:
- Factory Method: fabricar_lab2_hab, fabricar_lab2_hab_fm, fabricar_lab4_hab_fm
- Agregar personaje
- Condiciones de victoria/derrota
- Abrir/cerrar puertas
- Gestión de bichos
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego import Juego
from habitacion import Habitacion
from laberinto import Laberinto
from personaje import Personaje
from puerta import Puerta
from pared import Pared
from bicho import Bicho
from agresivo import Agresivo


class TestJuegoInit(unittest.TestCase):
    """Tests de inicialización del Juego."""

    def test_juego_sin_laberinto(self):
        """Un juego nuevo no tiene laberinto."""
        juego = Juego()
        self.assertIsNone(juego.laberinto)

    def test_juego_sin_personaje(self):
        """Un juego nuevo no tiene personaje."""
        juego = Juego()
        self.assertIsNone(juego.person)

    def test_juego_no_finalizado(self):
        """Un juego nuevo no está finalizado."""
        juego = Juego()
        self.assertFalse(juego.finalizado)

    def test_juego_sin_bichos(self):
        """Un juego nuevo tiene lista de bichos vacía."""
        juego = Juego()
        self.assertEqual(juego.bichos, [])


class TestFabricarLab2Hab(unittest.TestCase):
    """Tests de fabricar_lab2_hab — Factory Method."""

    def setUp(self):
        self.juego = Juego()
        self.juego.fabricar_lab2_hab()

    def test_laberinto_creado(self):
        """fabricar_lab2_hab crea un laberinto."""
        self.assertIsNotNone(self.juego.laberinto)

    def test_tiene_2_habitaciones(self):
        """El laberinto tiene exactamente 2 habitaciones."""
        self.assertIsNotNone(self.juego.obtener_habitacion(1))
        self.assertIsNotNone(self.juego.obtener_habitacion(2))

    def test_no_tiene_hab3(self):
        """No existe una habitación 3."""
        self.assertIsNone(self.juego.obtener_habitacion(3))


class TestFabricarLab2HabFM(unittest.TestCase):
    """Tests de fabricar_lab2_hab_fm — Factory Method con métodos fábrica."""

    def setUp(self):
        self.juego = Juego()
        self.juego.fabricar_lab2_hab_fm()

    def test_laberinto_creado(self):
        """fabricar_lab2_hab_fm crea un laberinto."""
        self.assertIsNotNone(self.juego.laberinto)

    def test_tiene_2_habitaciones(self):
        """El laberinto tiene 2 habitaciones."""
        self.assertIsNotNone(self.juego.obtener_habitacion(1))
        self.assertIsNotNone(self.juego.obtener_habitacion(2))

    def test_habitaciones_tienen_forma(self):
        """Las habitaciones creadas con FM tienen forma asignada."""
        hab1 = self.juego.obtener_habitacion(1)
        self.assertIsNotNone(hab1.forma)


class TestFabricarLab4HabFM(unittest.TestCase):
    """Tests de fabricar_lab4_hab_fm — Factory Method con 4 habitaciones."""

    def setUp(self):
        self.juego = Juego()
        self.juego.fabricar_lab4_hab_fm()

    def test_tiene_4_habitaciones(self):
        """El laberinto tiene 4 habitaciones."""
        for i in range(1, 5):
            self.assertIsNotNone(self.juego.obtener_habitacion(i))

    def test_no_tiene_hab5(self):
        """No existe una habitación 5."""
        self.assertIsNone(self.juego.obtener_habitacion(5))


class TestJuegoPersonaje(unittest.TestCase):
    """Tests de gestión del personaje en el Juego."""

    def setUp(self):
        self.juego = Juego()
        self.juego.fabricar_lab2_hab_fm()

    def test_agregar_personaje(self):
        """agregar_personaje crea un personaje con nombre."""
        self.juego.agregar_personaje("Héroe")
        self.assertIsNotNone(self.juego.person)
        self.assertEqual(self.juego.person.nombre, "Héroe")

    def test_personaje_en_hab1(self):
        """El personaje se coloca en la habitación 1."""
        self.juego.agregar_personaje("Héroe")
        hab1 = self.juego.obtener_habitacion(1)
        self.assertEqual(self.juego.person.posicion, hab1)

    def test_personaje_tiene_referencia_al_juego(self):
        """El personaje tiene referencia al juego."""
        self.juego.agregar_personaje("Héroe")
        self.assertEqual(self.juego.person.juego, self.juego)


class TestJuegoVictoriaDerrota(unittest.TestCase):
    """Tests de condiciones de victoria/derrota."""

    def setUp(self):
        self.juego = Juego()
        self.juego.fabricar_lab2_hab_fm()
        self.juego.agregar_personaje("Test")

    def test_gana_personaje(self):
        """gana_personaje marca finalizado y resultado victoria."""
        self.juego.gana_personaje()
        self.assertTrue(self.juego.finalizado)
        self.assertEqual(self.juego.resultado, "victoria")

    def test_muere_personaje(self):
        """muere_personaje marca finalizado y resultado derrota."""
        self.juego.muere_personaje()
        self.assertTrue(self.juego.finalizado)
        self.assertEqual(self.juego.resultado, "derrota")


class TestJuegoBichos(unittest.TestCase):
    """Tests de gestión de bichos en el Juego."""

    def setUp(self):
        self.juego = Juego()
        self.juego.fabricar_lab2_hab_fm()

    def test_agregar_bicho(self):
        """agregar_bicho añade el bicho a la lista."""
        bicho = Bicho()
        self.juego.agregar_bicho(bicho)
        self.assertIn(bicho, self.juego.bichos)

    def test_eliminar_bicho(self):
        """eliminar_bicho quita el bicho de la lista."""
        bicho = Bicho()
        self.juego.agregar_bicho(bicho)
        self.juego.eliminar_bicho(bicho)
        self.assertNotIn(bicho, self.juego.bichos)

    def test_hay_bichos_en_habitacion(self):
        """hay_bichos_en devuelve los bichos vivos en esa habitación."""
        bicho = Bicho()
        bicho.modo = Agresivo()
        hab1 = self.juego.obtener_habitacion(1)
        hab1.entrar(bicho)
        self.juego.agregar_bicho(bicho)

        resultado = self.juego.hay_bichos_en(hab1)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0], bicho)

    def test_hay_bichos_en_habitacion_vacia(self):
        """hay_bichos_en devuelve lista vacía si no hay bichos."""
        hab1 = self.juego.obtener_habitacion(1)
        resultado = self.juego.hay_bichos_en(hab1)
        self.assertEqual(len(resultado), 0)

    def test_buscar_personaje_misma_posicion(self):
        """buscar_personaje devuelve al personaje si está en la misma hab."""
        self.juego.agregar_personaje("Test")
        bicho = Bicho()
        hab1 = self.juego.obtener_habitacion(1)
        hab1.entrar(bicho)

        resultado = self.juego.buscar_personaje(bicho)
        self.assertEqual(resultado, self.juego.person)

    def test_buscar_personaje_distinta_posicion(self):
        """buscar_personaje devuelve None si no comparten posición."""
        self.juego.agregar_personaje("Test")
        bicho = Bicho()
        hab2 = self.juego.obtener_habitacion(2)
        hab2.entrar(bicho)

        resultado = self.juego.buscar_personaje(bicho)
        self.assertIsNone(resultado)


class TestJuegoPuertas(unittest.TestCase):
    """Tests de abrir/cerrar puertas globalmente."""

    def test_abrir_puertas(self):
        """abrir_puertas abre todas las puertas del laberinto."""
        juego = Juego()
        juego.fabricar_lab2_hab_fm()
        hab1 = juego.obtener_habitacion(1)

        juego.abrir_puertas()

        # La puerta sur de hab1 (accesible via forma) está abierta
        self.assertTrue(hab1.forma.sur.abierta)

    def test_cerrar_puertas(self):
        """cerrar_puertas cierra todas las puertas."""
        juego = Juego()
        juego.fabricar_lab2_hab_fm()
        juego.abrir_puertas()
        juego.cerrar_puertas()

        hab1 = juego.obtener_habitacion(1)
        self.assertFalse(hab1.forma.sur.abierta)


if __name__ == '__main__':
    unittest.main()
