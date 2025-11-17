# Proyecto Modelación de Sistema de Redes

import heapq as hq

calle = (50,55)
carrera = (10,15)

Javier = (54,14)
Andreina = (52,13)

carrera_11 = 7
carrera_12 = 7
carrera_13 = 7

carrera_calle = 5

# Discoteca The Darkness
lugar_1 = (50,14) 

# Bar La Pasión
lugar_2 = (54,11)

# Cervecería Mi Rolita
lugar_3 = (50,12)

calle_51 = 10

def obtener_tiempo_segmento(calle, carrera, direccion):
    """
    Obtiene el tiempo para recorrer un segmento.
    direccion: 'norte-sur' o 'este-oeste'
    """
    if direccion == 'norte-sur':
        # Moverse por una carrera (norte-sur)
        if carrera in [11, 12, 13]:
            return carrera_11
        else:
            return carrera_calle
    else:
        # Moverse por una calle (este-oeste)
        if calle == 51:
            return calle_51
        else:
            return carrera_calle

def construir_grafo():
    """Construye el grafo de la cuadrícula de Bogotá."""
    grafo = {}
    
    for c in range(calle[0], calle[1] + 1):  # Calles 50 a 55
        for cr in range(carrera[0], carrera[1] + 1):  # Carreras 10 a 15
            nodo = (c, cr)
            grafo[nodo] = []
            
            # Conexiones norte-sur (moverse por la carrera)
            # Al ir al sur, recorres la carrera desde c hasta c-1
            if c > calle[0]:  # Puede ir al sur
                vecino_sur = (c - 1, cr)
                tiempo = obtener_tiempo_segmento(c, cr, 'norte-sur')
                grafo[nodo].append((vecino_sur, tiempo))
            
            # Al ir al norte, recorres la carrera desde c hasta c+1
            if c < calle[1]:  # Puede ir al norte
                vecino_norte = (c + 1, cr)
                tiempo = obtener_tiempo_segmento(c, cr, 'norte-sur')
                grafo[nodo].append((vecino_norte, tiempo))
            
            # Conexiones este-oeste (moverse por la calle)
            # Al ir al este, recorres la calle desde cr hasta cr-1
            if cr > carrera[0]:  # Puede ir al este
                vecino_este = (c, cr - 1)
                tiempo = obtener_tiempo_segmento(c, cr, 'este-oeste')
                grafo[nodo].append((vecino_este, tiempo))
            
            # Al ir al oeste, recorres la calle desde cr hasta cr+1
            if cr < carrera[1]:  # Puede ir al oeste
                vecino_oeste = (c, cr + 1)
                tiempo = obtener_tiempo_segmento(c, cr, 'este-oeste')
                grafo[nodo].append((vecino_oeste, tiempo))
    
    return grafo

def dijkstra(grafo, inicio, fin, bloques_prohibidos=None):
    """
    Implementa el algoritmo de Dijkstra para encontrar el camino mínimo.
    
    Args:
        grafo: Diccionario que representa el grafo
        inicio: Tupla (calle, carrera) del punto de inicio
        fin: Tupla (calle, carrera) del punto de destino
        bloques_prohibidos: Conjunto de bloques que no se pueden usar (opcional)
    
    Returns:
        (tiempo_total, ruta): Tupla con el tiempo total y la lista de nodos de la ruta
    """
    if bloques_prohibidos is None:
        bloques_prohibidos = set()
    
    distancia = {nodo: float('inf') for nodo in grafo}
    distancia[inicio] = 0
    predecesores = {nodo: None for nodo in grafo}
    visitados = set()
    
    cola_prioridad = [(0, inicio)]
    
    while cola_prioridad:
        distancia_actual, nodo_actual = hq.heappop(cola_prioridad)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        if nodo_actual == fin:
            # Reconstruir la ruta
            ruta = []
            nodo = fin
            while nodo is not None:
                ruta.append(nodo)
                nodo = predecesores[nodo]
            ruta.reverse()
            return distancia_actual, ruta
        
        for vecino, peso in grafo[nodo_actual]:
            # Evitar bloques prohibidos (excepto origen y destino)
            if vecino in bloques_prohibidos and vecino != inicio and vecino != fin:
                continue
            
            if vecino not in visitados:
                distancia_nueva = distancia_actual + peso
                if distancia_nueva < distancia[vecino]:
                    distancia[vecino] = distancia_nueva
                    predecesores[vecino] = nodo_actual
                    hq.heappush(cola_prioridad, (distancia_nueva, vecino))
    
    return float('inf'), []

def obtener_bloques_ruta(ruta):
    """Obtiene el conjunto de bloques de una ruta (excepto el destino final)."""
    if not ruta:
        return set()
    return set(ruta[:-1])

def rutas_se_superponen(ruta1, ruta2):
    """Verifica si dos rutas se superponen en bloques intermedios."""
    bloques1 = obtener_bloques_ruta(ruta1)
    bloques2 = obtener_bloques_ruta(ruta2)
    return len(bloques1.intersection(bloques2)) > 0

def calcular_rutas_optimas(establecimiento):
    """
    Calcula las rutas óptimas para Javier y Andreína hacia un establecimiento.
    
    Args:
        establecimiento: Tupla (calle, carrera) del establecimiento destino
    
    Returns:
        Diccionario con las rutas, tiempos y información de sincronización
    """
    grafo = construir_grafo()
    
    # Calcular rutas más cortas sin restricciones
    tiempo_javier, ruta_javier = dijkstra(grafo, Javier, establecimiento)
    tiempo_andreina, ruta_andreina = dijkstra(grafo, Andreina, establecimiento)
    
    # Verificar si las rutas se superponen
    if rutas_se_superponen(ruta_javier, ruta_andreina):
        # Intentar encontrar rutas alternativas que no se superpongan
        bloques_javier = obtener_bloques_ruta(ruta_javier)
        tiempo_andreina_alt, ruta_andreina_alt = dijkstra(
            grafo, Andreina, establecimiento, bloques_prohibidos=bloques_javier
        )
        
        bloques_andreina = obtener_bloques_ruta(ruta_andreina)
        tiempo_javier_alt, ruta_javier_alt = dijkstra(
            grafo, Javier, establecimiento, bloques_prohibidos=bloques_andreina
        )
        
        # Elegir la opción que minimice el tiempo total (suma de tiempos)
        tiempo_total_opcion1 = tiempo_javier + tiempo_andreina_alt
        tiempo_total_opcion2 = tiempo_javier_alt + tiempo_andreina
        
        if tiempo_total_opcion1 <= tiempo_total_opcion2:
            ruta_andreina = ruta_andreina_alt
            tiempo_andreina = tiempo_andreina_alt
        else:
            ruta_javier = ruta_javier_alt
            tiempo_javier = tiempo_javier_alt
    
    # Determinar quién debe salir antes
    diferencia = abs(tiempo_javier - tiempo_andreina)
    quien_sale_antes = None
    tiempo_espera = 0
    
    if tiempo_javier > tiempo_andreina:
        quien_sale_antes = "Andreína"
        tiempo_espera = diferencia
    elif tiempo_andreina > tiempo_javier:
        quien_sale_antes = "Javier"
        tiempo_espera = diferencia
    
    return {
        'javier': {
            'ruta': ruta_javier,
            'tiempo': tiempo_javier,
            'origen': Javier
        },
        'andreina': {
            'ruta': ruta_andreina,
            'tiempo': tiempo_andreina,
            'origen': Andreina
        },
        'quien_sale_antes': quien_sale_antes,
        'tiempo_espera': tiempo_espera,
        'tiempo_total': max(tiempo_javier, tiempo_andreina),
        'se_superponen': rutas_se_superponen(ruta_javier, ruta_andreina)
    }

def formatear_ruta(ruta):
    """Formatea la ruta en un formato legible."""
    if not ruta:
        return "No se encontró ruta"
    
    pasos = []
    for i, (c, cr) in enumerate(ruta):
        if i == 0:
            pasos.append(f"    Inicio: Calle {c} con Carrera {cr}")
        elif i == len(ruta) - 1:
            pasos.append(f"    Destino: Calle {c} con Carrera {cr}")
        else:
            c_ant, cr_ant = ruta[i-1]
            if c > c_ant:
                direccion = "Norte"
            elif c < c_ant:
                direccion = "Sur"
            elif cr > cr_ant:
                direccion = "Oeste"
            else:
                direccion = "Este"
            pasos.append(f"    → {direccion} a Calle {c} con Carrera {cr}")
    
    return "\n".join(pasos)

def mostrar_resultados(establecimiento_nombre, establecimiento_desc, resultados):
    """Muestra los resultados de forma legible."""
    print("\n" + "="*70)
    print("ESTABLECIMIENTO:", establecimiento_nombre)
    print("Ubicacion:", establecimiento_desc)
    print("="*70)
    
    print("\nRUTA DE JAVIER:")
    print("Origen: Calle", resultados['javier']['origen'][0], "con Carrera", resultados['javier']['origen'][1])
    print("Tiempo total:", resultados['javier']['tiempo'], "minutos")
    print("Ruta:")
    print(formatear_ruta(resultados['javier']['ruta']))
    
    print("\nRUTA DE ANDREINA:")
    print("Origen: Calle", resultados['andreina']['origen'][0], "con Carrera", resultados['andreina']['origen'][1])
    print("Tiempo total:", resultados['andreina']['tiempo'], "minutos")
    print("Ruta:")
    print(formatear_ruta(resultados['andreina']['ruta']))
    
    print("\nSINCRONIZACION:")
    if resultados['quien_sale_antes']:
        print(resultados['quien_sale_antes'], "debe salir", resultados['tiempo_espera'], "minutos antes")
        print("para llegar simultaneamente al establecimiento.")
    else:
        print("Ambos pueden salir al mismo tiempo (mismo tiempo de recorrido).")
    
    print("\nTiempo total de caminata de la pareja:", resultados['tiempo_total'], "minutos")
    
    if resultados.get('se_superponen', False):
        print("\nADVERTENCIA: Las rutas se superponen en algunos bloques.")
    else:
        print("\nLas rutas no se superponen (no pueden ser vistos caminando juntos).")
    
    print("="*70 + "\n")

def main():
    """Función principal del programa."""
    establecimientos = {
        '1': {
            'nombre': 'Discoteca The Darkness',
            'ubicacion': lugar_1,
            'descripcion': 'Carrera 14 con Calle 50'
        },
        '2': {
            'nombre': 'Bar La Pasión',
            'ubicacion': lugar_2,
            'descripcion': 'Calle 54 con Carrera 11'
        },
        '3': {
            'nombre': 'Cervecería Mi Rolita',
            'ubicacion': lugar_3,
            'descripcion': 'Calle 50 con Carrera 12'
        }
    }
    
    print("\n" + "="*70)
    print("  OPTIMIZADOR DE RUTAS PARA JAVIER Y ANDREÍNA")
    print("  Bogotá - Sistema de Redes")
    print("="*70)
    print("\nEstablecimientos disponibles:")
    for id_est, info in establecimientos.items():
        print(f"  {id_est}. {info['nombre']} - {info['descripcion']}")
    
    print("\n" + "-"*70)
    print("Ubicaciones:")
    print(f"  Javier: Calle {Javier[0]} con Carrera {Javier[1]}")
    print(f"  Andreína: Calle {Andreina[0]} con Carrera {Andreina[1]}")
    print("-"*70)
    
    while True:
        opcion = input("\nSeleccione el establecimiento (1-3) o 'q' para salir: ").strip()
        
        if opcion.lower() == 'q':
            print("\n¡Hasta luego!")
            break
        
        if opcion not in ['1', '2', '3']:
            print("Opción inválida. Por favor seleccione 1, 2, 3 o 'q' para salir.")
            continue
        
        establecimiento = establecimientos[opcion]
        resultados = calcular_rutas_optimas(establecimiento['ubicacion'])
        
        if resultados:
            mostrar_resultados(
                establecimiento['nombre'],
                establecimiento['descripcion'],
                resultados
            )
        else:
            print("Error al calcular las rutas.")

main()
