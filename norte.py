"""
Módulo norte.

Define la orientación Norte del laberinto.
"""
from orientacion import Orientacion


class Norte(Orientacion):
    """Orientación Norte: mueve al bicho hacia el norte del contenedor."""

    def caminar(self, un_bicho):
        """Mueve un_bicho hacia el norte."""
        em = un_bicho.posicion.forma.norte
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado norte de un_cont."""
        un_cont.norte = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento norte de un_cont si existe."""
        if un_cont.norte:
            un_cont.norte.recorrer(un_bloque)
