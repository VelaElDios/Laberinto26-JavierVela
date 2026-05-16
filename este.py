"""
Módulo este.

Define la orientación Este del laberinto.
"""
from orientacion import Orientacion


class Este(Orientacion):
    """Orientación Este: mueve al bicho hacia el este del contenedor."""

    def caminar(self, un_bicho):
        """Mueve un_bicho hacia el este."""
        em = un_bicho.posicion.forma.este
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado este de un_cont."""
        un_cont.este = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento este de un_cont si existe."""
        if un_cont.este:
            un_cont.este.recorrer(un_bloque)
