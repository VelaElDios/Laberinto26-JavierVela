"""
Módulo noroeste.

Define la orientación Noroeste del laberinto (para formas Rombo).
"""
from orientacion import Orientacion


class Noroeste(Orientacion):
    """Orientación Noroeste: mueve al bicho hacia el noroeste del contenedor."""

    def caminar(self, un_bicho):
        """Mueve un_bicho hacia el noroeste."""
        em = un_bicho.posicion.forma.no
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado noroeste de un_cont."""
        un_cont.no = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento noroeste de un_cont si existe."""
        if getattr(un_cont, 'no', None):
            un_cont.no.recorrer(un_bloque)
