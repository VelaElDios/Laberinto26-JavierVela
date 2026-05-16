"""
Módulo sureste.

Define la orientación Sureste del laberinto (para formas Rombo).
"""
from orientacion import Orientacion


class Sureste(Orientacion):
    """Orientación Sureste: mueve al bicho hacia el sureste del contenedor."""

    def caminar(self, un_bicho):
        """Mueve un_bicho hacia el sureste."""
        em = un_bicho.posicion.forma.se
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        """Coloca un_em en el lado sureste de un_cont."""
        un_cont.se = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        """Aplica un_bloque al elemento sureste de un_cont si existe."""
        if getattr(un_cont, 'se', None):
            un_cont.se.recorrer(un_bloque)
