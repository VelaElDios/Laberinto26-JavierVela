"""
Módulo Orientaciones (compatibilidad).

Reexporta todas las orientaciones desde sus módulos individuales para
mantener la compatibilidad con importaciones existentes del tipo:

    from Orientaciones import Norte, Sur, Este, Oeste, ...
"""
from orientacion import Orientacion
from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from noreste import Noreste
from noroeste import Noroeste
from sureste import Sureste
from suroeste import Suroeste

__all__ = [
    "Orientacion",
    "Norte",
    "Sur",
    "Este",
    "Oeste",
    "Noreste",
    "Noroeste",
    "Sureste",
    "Suroeste",
]
