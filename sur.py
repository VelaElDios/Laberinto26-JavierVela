"""
Módulo sur.

Define la orientación Sur del laberinto.
"""
from orientacion import Orientacion


class Sur(Orientacion):
    """Orientación Sur: mueve al bicho hacia el sur del contenedor."""

    def caminar(self, un_bicho):
        """Mueve un_bicho hacia el sur."""
        em = un_bicho.posicion.forma.sur
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado sur de un_cont."""
        un_cont.sur = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento sur de un_cont si existe."""
        if un_cont.sur:
            un_cont.sur.recorrer(un_bloque)
