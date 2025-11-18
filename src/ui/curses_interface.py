import curses
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from algorithms.path_finder import PathFinder
from ui.graph_visualizer import GraphVisualizer

class CursesInterface:
    def __init__(self):
        self.finder = PathFinder()
        self.visualizer = GraphVisualizer()
        self.resultString = ""
    
    def get_dynamic_destination(self, stdscr):
        """Obtiene destino personalizado del usuario"""
        curses.echo()
        stdscr.erase()
        
        calle_str = ""
        carrera_str = ""

        # Obtener calle
        while True:
            stdscr.addstr("--- Ingresar Destino Personalizado ---\n")
            stdscr.addstr("La zona es entre la Calle 50 y la 55.\n\n")
            stdscr.addstr("Ingrese la Calle: ")
            stdscr.refresh()
            calle_str = stdscr.getstr().decode('utf-8').strip()
            
            try:
                calle_num = int(calle_str)
                if 50 <= calle_num <= 55:
                    break
                else:
                    stdscr.addstr(f"\nError: Calle debe estar entre 50-55. Presione una tecla.")
            except ValueError:
                stdscr.addstr(f"\nError: Debe ser un número. Presione una tecla.")
            
            stdscr.getch()
            stdscr.erase()

        # Obtener carrera 	
        stdscr.erase()
        while True:
            stdscr.addstr("--- Ingresar Destino Personalizado ---\n")
            stdscr.addstr(f"Calle ingresada: {calle_str}\n")
            stdscr.addstr("La zona es entre la Carrera 10 y la 15.\n\n")
            stdscr.addstr("Ingrese la Carrera: ")
            stdscr.refresh()
            carrera_str = stdscr.getstr().decode('utf-8').strip()

            try:
                carrera_num = int(carrera_str)
                if 10 <= carrera_num <= 15:
                    break
                else:
                    stdscr.addstr(f"\nError: Carrera debe estar entre 10-15. Presione una tecla.")
            except ValueError:
                stdscr.addstr(f"\nError: Debe ser un número. Presione una tecla.")

            stdscr.getch()
            stdscr.erase()

        curses.noecho()
        stdscr.erase()
        return f"{calle_str}{carrera_str}"
    
    def maximum(self, a, b):
        """Calcula la diferencia de tiempos"""
        self.resultString += "Para lograr llegar juntos es importante que "
        if a > b:
            c = str(a - b)
            self.resultString += f"Andreína salga {c} minutos después de Javier"
        elif a < b:
            c = str(b - a)
            self.resultString += f"Javier salga {c} minutos después de Andreína"
        else:
            self.resultString += "ambos salgan al mismo tiempo"
    
    def run(self, stdscr):
        """Ejecuta la interfaz principal"""

        bool = True
        while bool:
            self.resultString = ""
            
            # Menú de selección de destino
            classes = ["5012", "5014", "5411", "INPUT"]
            nombres = ["Cervecería Mi Rolita", "Discoteca The Darkness", 
                       "Bar La Pasión", "Otro Destino (Ingresar)"]
            
            decisiones = ["Ver otro recorrido", "Salir"]
            numeros = [1, 0]
            
            attributes = {}
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            attributes['normal'] = curses.color_pair(1)

            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            attributes['highlighted'] = curses.color_pair(2)

            c = 0
            option = 0
            while c != 10:
                stdscr.erase()
                stdscr.addstr("¿Qué recorrido quiere visualizar?\n", curses.A_UNDERLINE)
                for i in range(len(classes)):
                    if i == option:
                        attr = attributes['highlighted']
                    else:
                        attr = attributes['normal']
                    stdscr.addstr(f"{i + 1}. ")
                    stdscr.addstr(nombres[i] + '\n', attr)
                c = stdscr.getch()
                if c == curses.KEY_UP and option > 0:
                    option -= 1
                elif c == curses.KEY_DOWN and option < len(classes) - 1:
                    option += 1

            stdscr.erase()
            destino_id_flag = classes[option]
            destino_nombre = nombres[option]

            final_destination_id = ""
            if destino_id_flag == "INPUT":
                new_id = self.get_dynamic_destination(stdscr)
                final_destination_id = new_id
                self.resultString += f"El destino escogido por la pareja esta noche será {destino_nombre}:\n"
                self.resultString += f"Calle {final_destination_id[0:2]} con Carrera {final_destination_id[2:4]}\n\n"
            else:
                final_destination_id = destino_id_flag
                self.resultString += f"El destino escogido por la pareja esta noche será {destino_nombre}\n\n"
            
            # Usar el PathFinder en lugar de las funciones globales
            graphJ, graphA, timeJ, timeA = self.finder.find_optimal_paths(final_destination_id)
            
            # Añadir información de rutas al resultString
            self.resultString += f'El tiempo mínimo de Javier caminando es de {timeJ} minutos por la siguiente ruta: 	\n'
            self.resultString += self.finder.shortest_path(graphJ, graphJ.nodes_dict[final_destination_id]) + '\n\n'
            self.resultString += f'El tiempo mínimo de Andreína caminando es de {timeA} minutos por la siguiente ruta: \n'
            self.resultString += self.finder.shortest_path(graphA, graphA.nodes_dict[final_destination_id]) + '\n\n'
            
            self.maximum(timeJ, timeA)
            
            # --- CÁLCULO DE RECOMENDACIÓN PARA VISUALIZACIÓN ---
            recommendation_text = ""
            if timeJ > timeA:
                recommendation_text = f"Andreína debe salir {timeJ - timeA} minutos después de Javier"
            elif timeA > timeJ:
                recommendation_text = f"Javier debe salir {timeA - timeJ} minutos después de Andreína"
            else:
                recommendation_text = "Ambos deben salir al mismo tiempo"
            
            # Preguntar por visualización
            stdscr.addstr("\n\n¿Desea ver la visualización del grafo? (s/n): ")
            stdscr.refresh()
            if stdscr.getch() in [ord('s'), ord('S')]:
                path_javier = self.visualizer.path_to_node_list(graphJ, final_destination_id)
                path_andreina = self.visualizer.path_to_node_list(graphA, final_destination_id)
                
                # Pasamos los nuevos datos al visualizador
                self.visualizer.visualize(
                    graphJ, 
                    graphA, 
                    final_destination_id, 
                    path_javier, 
                    path_andreina,
                    timeJ, 
                    timeA,
                    recommendation_text
                )

            # Menú de decisiones
            attributes = {}
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            attributes['normal'] = curses.color_pair(1)

            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            attributes['highlighted'] = curses.color_pair(2)

            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            attributes['exit'] = curses.color_pair(3)

            c = 0
            option = 0
            while c != 10:
                stdscr.erase()
                stdscr.addstr(f"\n\n{self.resultString}\n")
                stdscr.addstr("\n\n\n¿Qué desea hacer?\n", curses.A_UNDERLINE)
                for i in range(len(decisiones)):
                    if i == option:
                        if option == 0:
                            attr = attributes['highlighted']
                        else:
                            attr = attributes['exit']
                    else:
                        attr = attributes['normal']
                    stdscr.addstr(f"{i + 1}. ")
                    stdscr.addstr(decisiones[i] + '\n', attr)
                c = stdscr.getch()
                if c == curses.KEY_UP and option > 0:
                    option -= 1
                elif c == curses.KEY_DOWN and option < len(decisiones) - 1:
                    option += 1
            
            if not (numeros[option]):
                bool = False