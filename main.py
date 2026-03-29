from Juego import Juego

def test_juego_basico():
    print("=== INICIALIZANDO JUEGO DE PRUEBA ===")
    juego = Juego()
    juego.fabricar_lab2_hab_fm()
    print("Laberinto construido con 2 habitaciones exitosamente.")
    
    print("\n=== AÑADIR PERSONAJE ===")
    juego.agregar_personaje("ProtaPython")
    
    print("\n=== RECORRER LABERINTO (Patrón Visitor/Iterator) ===")
    def imprimir_elemento(_elem):
        # Esta función vacía indica que ya estamos imprimiendo los elementos
        # dentro de los propios métodos recorrer().
        pass
        
    juego.laberinto.recorrer(imprimir_elemento)
    print("\n=== FIN DE LA PRUEBA ===")

if __name__ == "__main__":
    test_juego_basico()
