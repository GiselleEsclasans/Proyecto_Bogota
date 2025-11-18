def create_bogota_graph(graph):
    """
    Crea el grafo de Bogotá con calles 50-55 y carreras 10-15
    """
    # Crear nodos
    for calle in range(50, 56):
        for carrera in range(10, 16):
            graph.add_node(f"{calle}{carrera}")

    # Añadir aristas horizontales
    for calle in range(50, 56):
        for carrera in range(10, 15):
            weight = 5 if calle in [50, 52, 53, 54, 55] else 10
            graph.add_edge(f"{calle}{carrera}", f"{calle}{carrera+1}", weight)

    # Añadir aristas verticales
    for calle in range(50, 55):
        for carrera in range(10, 16):
            if (calle == 50 and carrera in [10, 14, 15]) or \
               (calle == 51 and carrera in [10, 14, 15]) or \
               (calle == 52 and carrera in [10, 14, 15]) or \
               (calle == 53 and carrera in [10, 14, 15]):
                weight = 5
            elif (calle == 54 and carrera in [10, 11, 14, 15]):
                weight = 7
            elif (calle == 54 and carrera in [12, 13]):
                weight = 9
            else:
                weight = 7
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