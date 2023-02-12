from classGraph import *

def parse_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove comments
    lines = [line for line in lines if not line.startswith('#')]
    lines = [line.strip() for line in lines]

    # Get the number of vertices, edges, minimum degree and maximum degree

    if len(lines[0]) > 3:
        nb_nodes, nb_edges, min_degree, max_degree = map(int, lines[0].split())
        lines = lines[1:]
    else:
        nb_nodes, nb_edges = map(int, lines[0].split())
        deg_min, deg_max = map(int, lines[1].split())
        lines = lines[2:]

    # Initialize the graph representation
    graph = {}

    # Iterate over the lines to build the graph representation
    for i in range(nb_nodes+1):
        line = lines[i]
        values = line.split()
        if len(values) == 2:
            u, v = map(int, values)
            if u not in graph:
                graph[u] = []
            graph[v].append((u, 1))
        else:
            # This line represents an edge
            u, v, weight = map(int, values)
            if u not in graph:
                graph[u] = []
            graph[u].append((v, weight))

    lines = lines[nb_nodes+1:]
    deg_nodes = []
    for line in lines:
        values = line.split()
        u ,v = map(int, values)
        deg_nodes.append(v)

    graph = Graph(nb_nodes, nb_edges, deg_min, deg_max, graph, deg_nodes)
    return graph