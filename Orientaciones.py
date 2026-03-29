from abc import ABC, abstractmethod

class Orientacion(ABC):
    """
    Orientacion define la interfaz de las orientaciones de los contenedores
    """
    @abstractmethod
    def caminar(self, un_bicho):
        pass

    @abstractmethod
    def poner_elemento_en_contenedor(self, un_em, un_cont):
        pass

    @abstractmethod
    def recorrer_en_contenedor(self, un_bloque, un_cont):
        pass

class SingletonOrientacion(Orientacion):
    _instancia = None

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("No se puede crear objeto con new, use default()")

    @classmethod
    def default(cls):
        if cls._instancia is None:
            cls._instancia = super(SingletonOrientacion, cls).__new__(cls)
        return cls._instancia

class Norte(SingletonOrientacion):
    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.norte
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        un_cont.norte = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        if un_cont.norte:
            un_cont.norte.recorrer(un_bloque)

class Sur(SingletonOrientacion):
    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.sur
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        un_cont.sur = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        if un_cont.sur:
            un_cont.sur.recorrer(un_bloque)

class Este(SingletonOrientacion):
    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.este
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        un_cont.este = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        if un_cont.este:
            un_cont.este.recorrer(un_bloque)

class Oeste(SingletonOrientacion):
    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.oeste
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        un_cont.oeste = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        if un_cont.oeste:
            un_cont.oeste.recorrer(un_bloque)

class Noreste(SingletonOrientacion):
    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.ne
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        un_cont.ne = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        if getattr(un_cont, 'ne', None):
            un_cont.ne.recorrer(un_bloque)

class Noroeste(SingletonOrientacion):
    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.no
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        un_cont.no = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        if getattr(un_cont, 'no', None):
            un_cont.no.recorrer(un_bloque)

class Sureste(SingletonOrientacion):
    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.se
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        un_cont.se = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        if getattr(un_cont, 'se', None):
            un_cont.se.recorrer(un_bloque)

class Suroeste(SingletonOrientacion):
    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.so
        em.entrar(un_bicho)

    def poner_elemento_en_contenedor(self, un_em, un_cont):
        un_cont.so = un_em

    def recorrer_en_contenedor(self, un_bloque, un_cont):
        if getattr(un_cont, 'so', None):
            un_cont.so.recorrer(un_bloque)
