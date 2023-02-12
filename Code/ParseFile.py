def parse_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove comments
    lines = [line for line in lines if not line.startswith('#')]
    lines = [line.strip() for line in lines]

    # Get the number of vertices, edges, minimum degree and maximum degree
    num_vertices, num_edges, min_degree, max_degree = map(int, lines[0].split())
    lines = lines[1:]

    # Initialize the graph representation
    graph = {}

    # Iterate over the lines to build the graph representation
    for line in lines:
        values = line.split()
        if len(values) == 2:
            # This line represents a vertex and its degree
            vertex = int(values[0])
            degree = int(values[1])
        else:
            # This line represents an edge
            u, v, weight = map(int, values)
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append((v, weight))
            graph[v].append((u, weight))

    
    return graph