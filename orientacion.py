"""
Módulo orientacion.

Define la clase base abstracta Orientacion con el patrón Singleton
aplicado directamente sobre ella: cada subclase concreta tendrá
una única instancia accesible mediante el método de clase default().
"""
from abc import ABC, abstractmethod


class Orientacion(ABC):
    """
    Orientacion es la clase base abstracta de todas las orientaciones.

    Implementa el patrón Singleton directamente: cada subclase concreta
    (Norte, Sur, Este, Oeste, …) mantendrá una única instancia propia,
    accesible a través del método de clase default().
    """

    _instancias: dict = {}

    def __new__(cls, *args, **kwargs):
        """Bloquea la creación directa con Orientacion().  Usa cls.default()."""
        if cls is Orientacion:
            raise TypeError("Orientacion es abstracta; instancia una subclase concreta.")
        # Si ya existe instancia para esta subclase, la devuelve
        if cls not in Orientacion._instancias:
            instance = super().__new__(cls)
            Orientacion._instancias[cls] = instance
        return Orientacion._instancias[cls]

    @classmethod
    def default(cls):
        """Devuelve la instancia única de la subclase concreta (Singleton)."""
        if cls not in Orientacion._instancias:
            # Llama a __new__ que ya gestiona el dict de instancias
            cls()
        return Orientacion._instancias[cls]

    @abstractmethod
    def caminar(self, un_bicho):
        """Mueve un_bicho en la dirección que representa esta orientación."""

    @abstractmethod
    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado correspondiente de un_cont."""

    @abstractmethod
    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento situado en este lado de un_cont."""
