"""
Módulo suroeste.

Define la orientación Suroeste del laberinto (para formas Rombo).
"""
from orientacion import Orientacion


class Suroeste(Orientacion):
    """Orientación Suroeste: mueve al bicho hacia el suroeste del contenedor."""

    def caminar(self, un_bicho):
        """Mueve un_bicho hacia el suroeste."""
        em = un_bicho.posicion.forma.so
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado suroeste de un_cont."""
        un_cont.so = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento suroeste de un_cont si existe."""
        if getattr(un_cont, 'so', None):
            un_cont.so.recorrer(un_bloque)
