def create_bogota_graph(graph):
    """
    Crea el grafo de Bogotá con calles 50-55 y carreras 10-15
    """
    # Crear nodos (Calle 50..55, Carrera 10..15)
    for calle in range(50, 56):
        for carrera in range(10, 16):
            graph.add_node(f"{calle}{carrera}")

    for calle in range(50, 56):
        for carrera in range(10, 15):
            weight = 10 if calle == 51 else 5
            graph.add_edge(f"{calle}{carrera}", f"{calle}{carrera+1}", weight)


    for calle in range(50, 55):
        for carrera in range(10, 16):
            weight = 7 if carrera in (11, 12, 13) else 5
            graph.add_edge(f"{calle}{carrera}", f"{calle+1}{carrera}", weight)

    return graph

# Puntos importantes del mapa
LANDMARKS = {
    "5414": ("Casa de Javier", "red"),
    "5213": ("Casa de Andreína", "green"), 
    "5012": ("Cervecería Mi Rolita", "orange"),
    "5014": ("Discoteca The Darkness", "purple"),
    "5411": ("Bar La Pasión", "brown")
}