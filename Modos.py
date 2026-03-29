import time

class Modo:
    """
    Modo define la interfaz de los comportamientos de los bichos
    """
    def actua(self, un_bicho):
        self.camina(un_bicho)
        self.ataca(un_bicho)
        self.duerme(un_bicho)

    def ataca(self, un_bicho):
        un_bicho.atacar()

    def camina(self, un_bicho):
        orien = un_bicho.obtener_orientacion_aleatoria()
        if orien:
            orien.caminar(un_bicho)

    def duerme(self, un_bicho):
        raise NotImplementedError

    def es_agresivo(self):
        return False

    def es_perezoso(self):
        return False


class Agresivo(Modo):
    """
    Agresivo es un modo del bicho más malo
    """
    def duerme(self, un_bicho):
        print(f"{un_bicho} duerme")
        time.sleep(1)

    def es_agresivo(self):
        return True

    def __str__(self):
        return "Agresivo"


class Perezoso(Modo):
    """
    Perezoso es un tipo de bicho que se mueve poco
    """
    def duerme(self, un_bicho):
        print(f"{un_bicho} duerme")
        time.sleep(3)

    def es_perezoso(self):
        return True

    def __str__(self):
        return "Perezoso"
