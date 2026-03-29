from ElementosMapa import Hoja

class Decorator(Hoja):
    """
    Es-una hoja (que es elemento del mapa) que tiene-un (decora) elemento del mapa
    """
    def __init__(self):
        super().__init__()
        self.em = None

    def entrar(self, alguien):
        if self.em:
            self.em.entrar(alguien)



class Bomba(Decorator):
    """
    Es un elemento del mapa que puede explotar si está activa
    """
    def __init__(self):
        super().__init__()
        self.activa = False

    def activar(self):
        print("Bomba activada")
        self.activa = True

    def desactivar(self):
        print("Bomba desactivada")
        self.activa = False

    def entrar(self, alguien=None):
        if self.activa:
            if alguien:
                print(f"{alguien}, te ha explotado una bomba")
                # ToDo: quitar vidas a alguien
            else:
                print("Ha explotado una bomba")
        
        # En el patrón Decorator, normalmente se llama al componente base
        # si hay uno, aunque Smalltalk no lo hacía explícitamente en el código visto.
        if self.em:
            self.em.entrar(alguien)

    def es_bomba(self):
        return True
