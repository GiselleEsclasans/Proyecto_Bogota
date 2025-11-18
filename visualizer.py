import networkx as nx
import matplotlib.pyplot as plt

def visualizar_rutas(javier_path, andreina_path, destino_id):
    # 1. Crear el grafo visual
    G = nx.Graph()
    
    pos = {}
    
    # Crear nodos y posiciones
    for calle in range(50, 56):
        for carrera in range(10, 16):
            node_id = f"{calle}{carrera}"
            # En un plano cartesiano: X = Carrera, Y = Calle
            pos[node_id] = (carrera, calle) 
            G.add_node(node_id)

    # 3. Crear aristas (La cuadrícula completa)
    # Esto es solo visual, para que se vea el mapa de fondo
    for calle in range(50, 56):
        for carrera in range(10, 16):
            u = f"{calle}{carrera}"
            # Conectar Norte (Calle + 1)
            if calle < 55:
                v = f"{calle+1}{carrera}"
                G.add_edge(u, v)
            # Conectar Oeste (Carrera + 1)
            if carrera < 15:
                v = f"{calle}{carrera+1}"
                G.add_edge(u, v)

    # 4. Configuración del dibujo
    plt.figure(figsize=(10, 8))
    
    # Dibujar la cuadrícula base (gris suave)
    nx.draw_networkx_nodes(G, pos, node_color='lightgrey', node_size=300)
    nx.draw_networkx_edges(G, pos, edge_color='lightgrey', width=1)
    
    # Etiquetas de los nodos (opcional, para ver coordenadas)
    nx.draw_networkx_labels(G, pos, font_size=8)

    # --- DIBUJAR RUTA DE JAVIER (AZUL) ---
    if javier_path and len(javier_path) > 1:
        # Obtener pares de nodos para las aristas (ej: A->B, B->C)
        j_edges = list(zip(javier_path, javier_path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=javier_path, node_color='skyblue', node_size=400)
        nx.draw_networkx_edges(G, pos, edgelist=j_edges, edge_color='blue', width=4, label='Javier')

    # --- DIBUJAR RUTA DE ANDREINA (ROSA) ---
    if andreina_path and len(andreina_path) > 1:
        a_edges = list(zip(andreina_path, andreina_path[1:]))
        # Los dibujamos un poco más pequeños o transparentes por si se solapan
        nx.draw_networkx_nodes(G, pos, nodelist=andreina_path, node_color='pink', node_size=250)
        nx.draw_networkx_edges(G, pos, edgelist=a_edges, edge_color='magenta', width=2, style='dashed', label='Andreína')

    # --- DIBUJAR PUNTOS CLAVE ---
    start_j = "5414"
    start_a = "5213"
    
    # Dibuja casa J
    nx.draw_networkx_nodes(G, pos, nodelist=[start_j], node_color='blue', node_shape='s', node_size=600, label='Casa Javier')
    # Dibuja casa A
    nx.draw_networkx_nodes(G, pos, nodelist=[start_a], node_color='magenta', node_shape='s', node_size=600, label='Casa Andreína')
    # Dibuja Destino
    nx.draw_networkx_nodes(G, pos, nodelist=[destino_id], node_color='gold', node_shape='*', node_size=800, label='Destino')

    plt.title(f"Ruta Óptima - Destino: Calle {destino_id[0:2]} Carrera {destino_id[2:4]}")
    plt.legend(loc='upper left') # Leyenda para entender colores
    plt.axis('off') # Ocultar ejes numéricos
    plt.tight_layout()
    
    # Muestra la ventana. El código se pausará aquí hasta que cierres la ventana.
    plt.show()