#!/usr/bin/env python3
"""
Script principal para ejecutar el proyecto de rutas en Bogotá
"""
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Ahora importar después de añadir al path
from main import main

if __name__ == "__main__":
    main()
    