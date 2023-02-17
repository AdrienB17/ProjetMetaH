from classGraph import *

def parse_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove comments
    lines = [line for line in lines if not line.startswith('#')]
    lines = [line.strip() for line in lines]
    # Get the number of vertices, edges, minimum degree and maximum degree

    ## !! len('10 17') > 3, split avant
    top = lines[0].split()
    if len(top) > 3:
        nb_nodes, nb_edges, min_degree, max_degree = map(int, lines[0].split())
        lines = lines[1:]
    else:
        nb_nodes, nb_edges = map(int, lines[0].split())
        deg_min, deg_max = map(int, lines[1].split())
        lines = lines[2:]

    # Initialize the graph representation
    graph = {}

    # Iterate over the lines to build the graph representation
    for i in range(nb_edges):
        line = lines[i]
        values = line.split()
        if len(values) == 2:
            u, v = map(int, values)
            if u not in graph:
                graph[u] = {}
            graph[v].update({u: 1})
            if v not in graph:
                graph[v] = {}
            graph[u].update({v: 1})
        else:
            # This line represents an edge
            u, v, weight = int(values[0]), int(values[1]), float(values[2])
            if u not in graph:
                graph[u] = {}
            graph[u].update({v: float(weight)})
            if v not in graph:
                graph[v] = {}
            graph[v].update({u: float(weight)})

    # Problème, le premier noeud doit être 0 pour respecter les indices du tableau

    lines = lines[nb_edges:]
    deg_nodes = []
    for j in range(nb_nodes):
        values = lines[j].split()
        u ,v = int(values[0]), float(values[1])
        deg_nodes.append(v)

    graphOut = Graph(nb_nodes, nb_edges, deg_min, deg_max, graph, deg_nodes)
    ## On trie les sommets dans l'ordre croissant.
    ## Si le graphe commence à 0 au lieu de 1, on réindexe.
    graphOut.graphRep = {k: v for k, v in sorted(graph.items(), key=lambda item: item[0])}
    try :
        graphOut[0]
        startWithZero = True
    except KeyError:
        startWithZero = False

    if not startWithZero :
       graphOut.graphRep = {(k-1) : v for k, v in graphOut.graphRep.items()} 
    return graphOut