"""
Módulo modo.

Define la clase base Modo, interfaz del patrón State para el comportamiento
de los bichos.
"""


class Modo:
    """
    Modo define la interfaz de los comportamientos de los bichos.
    Implementa el patrón State.
    """

    def actua(self, un_bicho):
        """Ejecuta el ciclo completo: camina, ataca y duerme."""
        self.camina(un_bicho)
        self.ataca(un_bicho)
        self.duerme(un_bicho)

    def ataca(self, un_bicho):
        """Hace que el bicho ataque a su enemigo."""
        un_bicho.atacar()

    def camina(self, un_bicho):
        """Mueve al bicho en una dirección aleatoria."""
        orien = un_bicho.obtener_orientacion_aleatoria()
        if orien:
            orien.caminar(un_bicho)

    def duerme(self, un_bicho):
        """Tiempo de espera entre acciones. Subclases lo implementan."""
        raise NotImplementedError

    def es_agresivo(self):
        """Devuelve True si este modo es agresivo."""
        return False

    def es_perezoso(self):
        """Devuelve True si este modo es perezoso."""
        return False
