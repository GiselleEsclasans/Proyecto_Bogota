
"""
Punto de entrada principal del proyecto de rutas en Bogotá
"""
import argparse
import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

from ui.curses_interface import CursesInterface
import curses
from ui.tk_interface import TkInterface

def main():
    parser = argparse.ArgumentParser(description='Sistema de rutas para Bogotá')
    parser.add_argument('--ui', choices=['curses', 'text', 'tk'], default='tk',
                       help='Tipo de interfaz de usuario')
    
    args = parser.parse_args()
    
    if args.ui == 'curses':
        interface = CursesInterface()
        curses.wrapper(interface.run)
    elif args.ui == 'tk':
        interface = TkInterface()
        interface.run()
    else:
        print("Interfaz texto no implementada aún")

if __name__ == "__main__":
    main()
    
