import sys
from models.graph import Graph

def dijkstra(graph: Graph, startNode: str):
    """Algoritmo de Dijkstra estándar"""
    graph.nodes_dict[startNode].set_distMin(0)
    
    nonVisitedNodes = list(graph.nodes_dict.keys())
    
    while nonVisitedNodes:
        # Encontrar nodo con menor distancia
        lessDist = sys.maxsize
        lessId = None
        
        for node_id in nonVisitedNodes:
            node = graph.nodes_dict[node_id]
            if node.distMin < lessDist:
                lessDist = node.distMin
                lessId = node_id
        
        if lessId is None:
            break
            
        # Relajar aristas
        current_node = graph.nodes_dict[lessId]
        distTillAct = current_node.distMin
        
        for neighbor, weight in current_node.adj.items():
            if not neighbor.visited:
                new_dist = distTillAct + weight
                if new_dist < neighbor.distMin:
                    neighbor.set_distMin(new_dist)
                    neighbor.set_predec(lessId)
        
        # Marcar como visitado
        current_node.visit()
        nonVisitedNodes.remove(lessId)

def restricted_dijkstra(graph: Graph, startNode: str, pred: str, target: str):
    """Dijkstra con restricciones para evitar ciertos caminos"""
    graph.nodes_dict[startNode].set_distMin(0)
    nonVisitedNodes = list(graph.nodes_dict.keys())
    
    while nonVisitedNodes:
        lessDist = sys.maxsize
        lessId = None
        
        for node_id in nonVisitedNodes:
            node = graph.nodes_dict[node_id]
            if node.distMin < lessDist:
                lessDist = node.distMin
                lessId = node_id
        
        if lessId is None:
            break
            
        current_node = graph.nodes_dict[lessId]
        distTillAct = current_node.distMin
        
        for neighbor, weight in current_node.adj.items():
            if (not neighbor.visited and 
                (neighbor.id != target or lessId != pred)):
                
                new_dist = distTillAct + weight
                if new_dist < neighbor.distMin:
                    neighbor.set_distMin(new_dist)
                    neighbor.set_predec(lessId)
        
        current_node.visit()
        nonVisitedNodes.remove(lessId)