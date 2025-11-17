import sys
from node import *
from graph import *
from edges import *
# from test import *
import curses

nodes:int = 0
nodesId = []
edges = {}
graphJ : Graph
graphA : Graph
graphJ1 : Graph
graphA2 : Graph
startNodeJ = "5414"
startNodeA = "5213"
Brewery = "5012"
Disco = "5014"
Bar = "5411"
resultString:str = ""

def maximum(a, b, stdscr):
     
    global resultString

    resultString += "Para lograr llegar juntos es importante que "
    if a > b:
        c=str(a-b)
        resultString = resultString + "Andreína salga "+c+" minutos después de Javier"
        # stdscr.addstr("Andreína debe salir "+c+"min después de Javier para llegar al mismo tiempo", curses.A_UNDERLINE)
        
        return 
    elif a< b:
        c=str(b-a)
        resultString = resultString + "Javier debe salga "+c+" minutos después de Andreína"
        
        
        return
    else: 
        resultString = resultString + "Ambos salgan al mismo tiempo"
     
def create():
    global graphJ 
    global graphA 
    global graphA2
    global graphJ1
    global nodes
    global nodesId
    graphJ = Graph()
    graphA = Graph()
    graphJ1 = Graph()
    graphA2 = Graph()
    for i in range (50,56):

        for j in range (10, 16):
            # nodeX = Node(f'{i}:{j}')
            # nodes.append(nodeX)
            # nodesId.append(nodeX.id)
            graphJ.add_node(f'{i}{j}')
            graphA.add_node(f'{i}{j}')
            graphJ1.add_node(f'{i}{j}')
            graphA2.add_node(f'{i}{j}')
            nodesId.append(f'{i}{j}')
            # print(f'calle {i} con carrera {j}')
    # print(graphA.nodes_dict)
    # print(nodesId)
    
def shortestPath(graphX: Graph,nodeActual: Node):
    # print('num'+nodeActual.id)
    # print(nodeActual.distMin)
    if not (nodeActual.distMin == 0 ) :
        
        return  shortestPath (graphX, graphX.nodes_dict[nodeActual.pred])+ " ==>" + f' Calle {nodeActual.id[0:2]} con carrera {nodeActual.id[2:4]}' 
    return f'Calle {nodeActual.id[0:2]} con carrera {nodeActual.id[2:4]}' 

def shortestPath2(graphX: Graph,nodeActual: Node):
    # print('num'+nodeActual.id)
    # print(nodeActual.distMin)
    if not (nodeActual.distMin == 0 ) :
        
        return  shortestPath (graphX, graphX.nodes_dict[nodeActual.pred])+ "luego va a" + f'la calle {nodeActual.id[0:2]} con carrera {nodeActual.id[2:4]} y habra llegado a su destino' 
    return f'Comienza en la calle {nodeActual.id[0:2]} con carrera {nodeActual.id[2:4]}' 

def restrictedDijkstra(graphX: Graph, startNode:str, pred:str, target: str):
    graphX.nodes_dict[startNode].set_distMin(0)
    #---------------------------------------------------------------
    #print(graphX.nodes_dict)
    #---------------------------------------------------------------
    nonVisitedNodes = []
    if len(nodesId)<1:
        #---------------------------------------------------------------
        #print('entro')
        #---------------------------------------------------------------
        for i in graphX.nodes_dict.keys():
            nonVisitedNodes.append(i)
    else:
        nonVisitedNodes = nodesId

    while len(nonVisitedNodes) >0:
        lessDist: int = sys.maxsize
        lessId: str
        
        # print(nonVisitedNodes)
        for i in range (len(nonVisitedNodes)):
            
            curValue = graphX.nodes_dict[nonVisitedNodes[i]].distMin
            # print(curValue)
            # print(curValue)
            if curValue < lessDist:
                lessDist = curValue
                lessId = nonVisitedNodes[i]
        
        # visit graphX.nodes_dict[lessId]
        items = graphX.nodes_dict[lessId].adj.items()
        distTillAct: int = graphX.nodes_dict[lessId].distMin
        for j,k in ((items)):
            
            
            # if lessId == pred:
            #     print(f'PRED: lessId={lessId}, pred={pred}, j={j.id}, target={target}')
            
                # print(curValue)
            if (not (j.visited) and (j.id != target or lessId != pred)) :
                
                # if j.id == target:
                #     print(f'lessId={lessId}, pred={pred}, j={j.id}, target={target}, visited={graphX.nodes_dict[target].visited}')
                sum = distTillAct + (k)
                if (sum < j.distMin):
                
                    j.set_distMin(sum)
                    j.set_predec(lessId) 
        #mark visited actual node
        
        graphX.nodes_dict[lessId].visit()
        nonVisitedNodes.remove(lessId)
    #---------------------------------------------------------------
    #print(nonVisitedNodes)
    #print(nodesId)
    #---------------------------------------------------------------

    return

def dijkstra(graphX: Graph, startNode:str):
    graphX.nodes_dict[startNode].set_distMin(0)
    #---------------------------------------------------------------
    #print(graphX.nodes_dict)
    #---------------------------------------------------------------
    nonVisitedNodes = []
    if len(nodesId)<1:
        #---------------------------------------------------------------
        #print('entro')
        #---------------------------------------------------------------
        for i in graphX.nodes_dict.keys():
            nonVisitedNodes.append(i)
    else:
        nonVisitedNodes = nodesId

    while len(nonVisitedNodes) >0:
        lessDist: int = sys.maxsize
        lessId: str
        
        for i in range (len(nonVisitedNodes)):
            
            curValue = graphX.nodes_dict[nonVisitedNodes[i]].distMin
            if curValue < lessDist:
                lessDist = curValue
                lessId = nonVisitedNodes[i]  
        # visit graphX.nodes_dict[lessId]
        items = graphX.nodes_dict[lessId].adj.items()
        distTillAct: int = graphX.nodes_dict[lessId].distMin
        for j,k in ((items)):
            if not ((j).visited):
                sum = distTillAct + (k)
                if (sum < j.distMin):
                    j.set_distMin(sum)
                    j.set_predec(lessId) 
        #mark visited actual node

        graphX.nodes_dict[lessId].visit()
        nonVisitedNodes.remove(lessId)
    #---------------------------------------------------------------
    #print(nonVisitedNodes)
    #print(nodesId)
    #---------------------------------------------------------------

    return 0

def path(finalNode:str, stdscr):
    global resultString
    create()
    #aristas javier

    #fila 50
    edgesFunct(graphA)
    edgesFunct(graphJ)
    edgesFunct(graphA2)
    edgesFunct(graphJ1)
    # print('a')

    #---------------------------------------------------------------
    #print("viene javier")
    #---------------------------------------------------------------
    # print('primer dijks')
    dijkstra(graphA, startNodeA)
    # print('segundo dijks')
    restrictedDijkstra(graphJ, startNodeJ, graphA.nodes_dict[finalNode].pred, finalNode)
    # print('tercer dijks')

    dijkstra(graphJ1, startNodeJ)
    # print('cuarto dijks')

    restrictedDijkstra(graphA2, startNodeA, graphJ1.nodes_dict[finalNode].pred, finalNode)


    destination :str = finalNode
    # destination :str = "5011"
    # destination :str = "5113"
    # print(graphA.nodes_dict)
    firstMax = max(graphA.nodes_dict[destination].distMin, graphJ.nodes_dict[destination].distMin)
    secondMax = max(graphJ1.nodes_dict[destination].distMin, graphA2.nodes_dict[destination].distMin)

    if(firstMax <= secondMax):
        pathAndreinaSum = graphA.nodes_dict[destination].distMin
        pathJavierSum = graphJ.nodes_dict[destination].distMin
        resultString = resultString + f'El tiempo mínimo de Javier caminando es de {pathJavierSum} minutos por la siguiente ruta:  \n{shortestPath(graphJ, graphJ.nodes_dict[destination])} \n\nEl tiempo mínimo de Andreína caminando es de {pathAndreinaSum} minutos por la siguiente ruta: \n{shortestPath(graphA, graphA.nodes_dict[destination])}\n\n'
        
        
    else:
        pathAndreinaSum = graphA2.nodes_dict[destination].distMin
        pathJavierSum = graphJ1.nodes_dict[destination].distMin
    
        resultString = resultString +  f'El tiempo mínimo de Javier caminando es de {pathJavierSum} minutos por la siguiente ruta: \n{shortestPath(graphJ1, graphJ1.nodes_dict[destination])} \n\nEl tiempo mínimo de Andreína caminando es de {pathAndreinaSum} minutos por la siguiente ruta: \n{shortestPath(graphA2, graphA2.nodes_dict[destination])}\n\n'
    
    maximum(pathJavierSum,pathAndreinaSum, stdscr)
    return 

# NO SE USA
# def menu():
#     loop = "0"
#     while loop == "0":
#         print("Javier y Andreína deben escoger su destino.")
#         print ("1. Ir al Brewery.")
#         print ("2. Ir a la Disco.")
#         print ("3. Ir al Bar.")
#         destino = input("Ingrese 1,2 o 3, según corresponda: ")
#         if destino == "1":
#             destino = Brewery
#             print ("Javier y Andreína irán al Brewery"+ "\n"*5)
#             path(destino)
#             print("Oprime 0 si deseas escoger un nuevo destino.")
#             loop = input()
#             print("\n"*5)
#         elif destino == "2":
#             destino = Disco
#             print ("Javier y Andreína irán a la Disco"+ "\n"*5)
#             path(destino)
#             print("Oprime 0 si deseas escoger un nuevo destino.")
#             loop = input()
#             print("\n"*5)
#         elif destino == "3":
#             destino = Bar
#             print ("Javier y Andreína irán al Bar"+ "\n"*5)
#             path(destino)
#             print("Oprime 0 si deseas escoger un nuevo destino.")
#             loop = input()
#             print("\n"*5)

#         else:
#             print ("I'm sorry, I didn't get that" + "\n"*5)

def get_dynamic_destination(stdscr):
    """
    Usa curses para pedir al usuario una Calle y Carrera,
    validarlas y devolver el ID del nodo (ej: "5213").
    """
    curses.echo()  # Activar que se vea lo que el usuario escribe
    stdscr.erase()
    
    calle_str = ""
    carrera_str = ""

    # --- Bucle para obtener la Calle ---
    while True:
        stdscr.addstr("--- Ingresar Destino Personalizado ---\n")
        stdscr.addstr("La zona es entre la Calle 50 y la 55.\n\n")
        stdscr.addstr("Ingrese la Calle: ")
        stdscr.refresh()
        calle_str = stdscr.getstr().decode('utf-8').strip()
        
        # Validación
        try:
            calle_num = int(calle_str)
            if 50 <= calle_num <= 55:
                break  # Input válido, salir del bucle
            else:
                stdscr.addstr(f"\nError: '{calle_str}' no está entre 50 y 55. Presione una tecla para reintentar.\n")
        except ValueError:
            stdscr.addstr(f"\nError: '{calle_str}' no es un número. Presione una tecla para reintentar.\n")
        
        stdscr.getch()  # Esperar que el usuario presione una tecla
        stdscr.erase()

    # --- Bucle para obtener la Carrera ---
    stdscr.erase()
    while True:
        stdscr.addstr("--- Ingresar Destino Personalizado ---\n")
        stdscr.addstr(f"Calle ingresada: {calle_str}\n")
        stdscr.addstr("La zona es entre la Carrera 10 y la 15.\n\n")
        stdscr.addstr("Ingrese la Carrera: ")
        stdscr.refresh()
        carrera_str = stdscr.getstr().decode('utf-8').strip()

        # Validación
        try:
            carrera_num = int(carrera_str)
            if 10 <= carrera_num <= 15:
                break  # Input válido, salir del bucle
            else:
                stdscr.addstr(f"\nError: '{carrera_str}' no está entre 10 y 15. Presione una tecla para reintentar.\n")
        except ValueError:
            stdscr.addstr(f"\nError: '{carrera_str}' no es un número. Presione una tecla para reintentar.\n")

        stdscr.getch()  # Esperar que el usuario presione una tecla
        stdscr.erase()

    curses.noecho()  # Desactivar el echo
    stdscr.erase()
    
    # Devolver el ID formateado
    return f"{calle_str}{carrera_str}"

# SE USA MENU 2:
def menu2():
    #ANTES
    # classes = [Brewery, Disco, Bar]
    # nombres = ["Cervecería Mi Rolita", "Discoteca The Darkness", "Bar La Pasión"]

    # AHORA (AÑADE LA LÍNEA 4):
    classes = [Brewery, Disco, Bar, "INPUT"]
    nombres = ["Cervecería Mi Rolita", "Discoteca The Darkness", "Bar La Pasión", "Otro Destino (Ingresar)"]

    decisiones = ["Ver otro recorrido", "Salir"]
    numeros = [1,0]
    def character(stdscr):

        bool = True
        while bool:
            global resultString
            resultString = ""
            attributes = {}
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            attributes['normal'] = curses.color_pair(1)

            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            attributes['highlighted'] = curses.color_pair(2)

            c = 0  # last character read
            option = 0  # the current option that is marked
            while c != 10:  # Enter in ascii
                stdscr.erase()
                stdscr.addstr("¿Qué recorrido quiere visualizar?\n", curses.A_UNDERLINE)
                for i in range(len(classes)):
                    if i == option:
                        attr = attributes['highlighted']
                    else:
                        attr = attributes['normal']
                    stdscr.addstr("{0}. ".format(i + 1))
                    stdscr.addstr(nombres[i] + '\n', attr)
                c = stdscr.getch()
                if c == curses.KEY_UP and option > 0:
                    option -= 1
                elif c == curses.KEY_DOWN and option < len(classes) - 1:
                    option += 1

            #ANTES
            # stdscr.erase()
            # resultString += f"El destino escogido por la pareja esta noche será {nombres[option]}\n\n"
            # # path("5113", stdscr)
            # path(classes[option], stdscr)

            # AHORA (REEMPLAZA LO ANTERIOR CON ESTE BLOQUE):
            stdscr.erase()
            destino_id_flag = classes[option]
            destino_nombre = nombres[option]

            final_destination_id = ""  # El ID real que se pasará a path()

            if destino_id_flag == "INPUT":
                # Si el usuario eligió "Otro Destino", llamamos a nuestra nueva función
                new_id = get_dynamic_destination(stdscr) 
                final_destination_id = new_id
                
                # Construimos el string de resultado para el destino dinámico
                resultString += f"El destino escogido por la pareja esta noche será {destino_nombre}:\n"
                resultString += f"Calle {final_destination_id[0:2]} con Carrera {final_destination_id[2:4]}\n\n"
            else:
                # Lógica original para los destinos fijos
                final_destination_id = destino_id_flag
                resultString += f"El destino escogido por la pareja esta noche será {destino_nombre}\n\n"
            
            # Llamada unificada a path(), que ahora funciona con IDs fijos o dinámicos
            path(final_destination_id, stdscr)
            
            # --- FIN DEL BLOQUE MODIFICADO ---

            attributes = {}
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            attributes['normal'] = curses.color_pair(1)

            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            attributes['highlighted'] = curses.color_pair(2)

            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            attributes['exit'] = curses.color_pair(3)

            c = 0  # last character read
            option = 0  # the current option that is marked
            while c != 10:  # Enter in ascii
                stdscr.erase()
                stdscr.addstr(f"\n\n{resultString}\n")
                stdscr.addstr("\n\n\n¿Qué desea hacer?\n", curses.A_UNDERLINE)
                for i in range(len(decisiones)):
                    if i == option:
                        if option == 0:
                            attr = attributes['highlighted']
                        else:
                            attr = attributes['exit']
                    else:
                        attr = attributes['normal']
                    stdscr.addstr("{0}. ".format(i + 1))
                    stdscr.addstr(decisiones[i] + '\n', attr)
                c = stdscr.getch()
                if c == curses.KEY_UP and option > 0:
                    option -= 1
                elif c == curses.KEY_DOWN and option < len(decisiones) - 1:
                    option += 1
            
            if not (numeros[option]):
                bool = False
                
    def menucito():

        curses.wrapper(character)
    menucito()

def main():
    menu2()
        
main()
