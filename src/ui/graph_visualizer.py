import matplotlib.pyplot as plt
import networkx as nx
from data.city_map import LANDMARKS

class GraphVisualizer:
    def __init__(self):
        self.fig = None
        self.ax = None
    
    def extract_graph_data(self, graph):
        """Extrae datos del grafo para visualización"""
        nodes = list(graph.nodes_dict.keys())
        edges = []
        
        for node_id, node in graph.nodes_dict.items():
            for neighbor, weight in node.adj.items():
                edge = (node_id, neighbor.id, weight)
                if edge not in edges and (neighbor.id, node_id, weight) not in edges:
                    edges.append(edge)
        
        return {'nodes': nodes, 'edges': edges}
    
    def path_to_node_list(self, graph, destination):
        """Convierte un camino en lista de nodos"""
        from algorithms.path_finder import PathFinder
        finder = PathFinder()
        path_str = finder.shortest_path(graph, graph.nodes_dict[destination])
        
        nodes = []
        parts = path_str.split('==>')
        for part in parts:
            part = part.strip()
            if 'Calle' in part and 'carrera' in part:
                calle = part.split('Calle ')[1].split(' ')[0]
                carrera = part.split('carrera ')[1]
                nodes.append(f"{calle}{carrera}")
        return nodes
    
    def visualize(self, graphJ, graphA, destination, path_javier, path_andreina):
        """Visualiza el grafo con las rutas"""
        graph_data = self.extract_graph_data(graphJ)
        
        G = nx.Graph()
        for node_id in graph_data['nodes']:
            G.add_node(node_id)
        
        for edge in graph_data['edges']:
            G.add_edge(edge[0], edge[1], weight=edge[2])
        
        # Posiciones basadas en coordenadas
        # Queremos: norte = Calle 55 en la parte superior, sur = Calle 50 en la parte inferior,
        #           izquierda = Carrera 15 (oeste), derecha = Carrera 10 (este).
        # Para lograr esto en un sistema de coordenadas donde X crece a la derecha y Y crece hacia arriba:
        # - X debe ser mayor para Carrera 10 y menor para Carrera 15 -> x = 15 - carrera
        # - Y debe ser mayor para Calle 55 y menor para Calle 50 -> y = calle - 50
        pos = {}
        for node in G.nodes():
            calle = int(node[:2])
            carrera = int(node[2:])
            x = 15 - carrera
            y = calle - 50
            pos[node] = (x, y)
        
        plt.figure(figsize=(14, 10))
        
        # Dibujar grafo base
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=400, alpha=0.7)
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                              alpha=0.4, width=1)
        nx.draw_networkx_labels(G, pos, font_size=7)
        
        # Resaltar puntos importantes
        for node_id, (label, color) in LANDMARKS.items():
            if node_id in G.nodes():
                nx.draw_networkx_nodes(G, pos, nodelist=[node_id], 
                                      node_color=color, node_size=600,
                                      label=label)
        
        # Dibujar rutas
        if path_javier:
            path_edges_j = [(path_javier[i], path_javier[i+1]) 
                           for i in range(len(path_javier)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges_j, 
                                  edge_color='red', width=3, alpha=0.8,
                                  label='Ruta Javier')
        
        if path_andreina:
            path_edges_a = [(path_andreina[i], path_andreina[i+1]) 
                           for i in range(len(path_andreina)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges_a, 
                                  edge_color='green', width=3, alpha=0.8,
                                  label='Ruta Andreína')
        
        # Destino
        if destination in G.nodes():
            nx.draw_networkx_nodes(G, pos, nodelist=[destination], 
                                  node_color='yellow', node_size=700,
                                  edgecolors='black', linewidths=2,
                                  label='Destino')
        
        plt.title("Mapa de Bogotá - Rutas de Javier y Andreína", fontsize=14)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.axis('off')
        plt.tight_layout()
        plt.show()