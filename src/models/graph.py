from .node import Node

class Graph:
    def __init__(self):
        self.nodes_dict = {}
        self.num_vertices = 0

    def add_node(self, nodeId: str) -> Node:
        self.num_vertices += 1
        new_node = Node(nodeId)
        self.nodes_dict[nodeId] = new_node
        return new_node

    def add_edge(self, nodeFrom: str, nodeTo: str, time: int):
        if nodeFrom not in self.nodes_dict:
            self.add_node(nodeFrom)
        if nodeTo not in self.nodes_dict:
            self.add_node(nodeTo)

        self.nodes_dict[nodeFrom].add_neighbor(self.nodes_dict[nodeTo], time)
        self.nodes_dict[nodeTo].add_neighbor(self.nodes_dict[nodeFrom], time)

    def get_node(self, node_id: str) -> Node:
        return self.nodes_dict.get(node_id)

    def get_all_nodes(self):
        return list(self.nodes_dict.keys())

    def debug(self):
        for node_id, node in self.nodes_dict.items():
            print(f"{node_id}: {node.adj}")