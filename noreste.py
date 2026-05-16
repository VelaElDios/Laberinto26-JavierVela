"""
Módulo noreste.

Define la orientación Noreste del laberinto (para formas Rombo).
"""
from orientacion import Orientacion


class Noreste(Orientacion):
    """Orientación Noreste: mueve al bicho hacia el noreste del contenedor."""

    def caminar(self, un_bicho):
        """Mueve un_bicho hacia el noreste."""
        em = un_bicho.posicion.forma.ne
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado noreste de un_cont."""
        un_cont.ne = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento noreste de un_cont si existe."""
        if getattr(un_cont, 'ne', None):
            un_cont.ne.recorrer(un_bloque)
