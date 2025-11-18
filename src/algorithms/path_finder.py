import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.graph import Graph
from algorithms.dijkstra import dijkstra, restricted_dijkstra
from data.city_map import create_bogota_graph

class PathFinder:
    def __init__(self):
        self.startNodeJ = "5414"
        self.startNodeA = "5213"
        self.landmarks = {
            "5012": "Cervecería Mi Rolita",
            "5014": "Discoteca The Darkness", 
            "5411": "Bar La Pasión"
        }
    
    def create_graphs(self):
        """Crea los cuatro grafos necesarios para el cálculo"""
        graphJ = Graph()
        graphA = Graph()
        graphJ1 = Graph()
        graphA2 = Graph()
        
        return graphJ, graphA, graphJ1, graphA2
    
    def shortest_path(self, graph: Graph, nodeActual) -> str:
        """Reconstruye el camino más corto como string"""
        if nodeActual.distMin != 0 and nodeActual.pred:
            pred_node = graph.nodes_dict[nodeActual.pred]
            return (self.shortest_path(graph, pred_node) + 
                   " ==> " + f'Calle {nodeActual.id[0:2]} con carrera {nodeActual.id[2:4]}')
        return f'Calle {nodeActual.id[0:2]} con carrera {nodeActual.id[2:4]}'
    
    def find_optimal_paths(self, finalNode: str):
        """Encuentra los caminos óptimos para Javier y Andreína"""
        graphJ, graphA, graphJ1, graphA2 = self.create_graphs()
        
        # Crear grafos con el mapa
        create_bogota_graph(graphA)
        create_bogota_graph(graphJ)
        create_bogota_graph(graphA2)
        create_bogota_graph(graphJ1)
        
        # Calcular caminos
        dijkstra(graphA, self.startNodeA)
        restricted_dijkstra(graphJ, self.startNodeJ, 
                           graphA.nodes_dict[finalNode].pred, finalNode)
        
        dijkstra(graphJ1, self.startNodeJ)
        restricted_dijkstra(graphA2, self.startNodeA, 
                           graphJ1.nodes_dict[finalNode].pred, finalNode)
        
        # Determinar mejor combinación
        firstMax = max(graphA.nodes_dict[finalNode].distMin, 
                      graphJ.nodes_dict[finalNode].distMin)
        secondMax = max(graphJ1.nodes_dict[finalNode].distMin, 
                       graphA2.nodes_dict[finalNode].distMin)
        
        if firstMax <= secondMax:
            return (graphJ, graphA, 
                    graphJ.nodes_dict[finalNode].distMin,
                    graphA.nodes_dict[finalNode].distMin)
        else:
            return (graphJ1, graphA2,
                    graphJ1.nodes_dict[finalNode].distMin,
                    graphA2.nodes_dict[finalNode].distMin)