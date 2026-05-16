"""
Módulo oeste.

Define la orientación Oeste del laberinto.
"""
from orientacion import Orientacion


class Oeste(Orientacion):
    """Orientación Oeste: mueve al bicho hacia el oeste del contenedor."""

    def caminar(self, un_bicho):
        """Mueve un_bicho hacia el oeste."""
        em = un_bicho.posicion.forma.oeste
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado oeste de un_cont."""
        un_cont.oeste = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento oeste de un_cont si existe."""
        if un_cont.oeste:
            un_cont.oeste.recorrer(un_bloque)
