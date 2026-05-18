"""
Configuración compartida de los tests.

Añade el directorio raíz del proyecto al sys.path para que los imports
funcionen correctamente desde la carpeta tests/.
"""
import sys
import os

# Añade la raíz del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
