"""
Módulo armario.

Define la clase Armario, contenedor secundario dentro de una habitación.
"""
from contenedor import Contenedor


class Armario(Contenedor):
    """
    Armario es un contenedor que vive dentro de una habitación.
    Tiene una puerta al este que lo comunica con su contenedor padre.
    """
