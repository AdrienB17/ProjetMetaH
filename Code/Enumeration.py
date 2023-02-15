from itertools import combinations
from math import ceil, floor

def partition_graph(graph):
    def check_valid_partition(partition, Graphe):
        graph = Graphe.graphRep
        # Calculate the sum of weights between vertices in different classes
        sum_of_weights = 0
        n = len(graph)
        for i in graph:
            for j in graph[i]:
                if partition[i] != partition[j]:
                    if j in graph[i]:
                        sum_of_weights += graph[i][j]
        # Check if the sum of weights is minimal and the classes are roughly equally populated
        return sum_of_weights <= sum([sum(graph[i].values()) for i in graph]) and abs(
            len([x for x in partition if x == 0]) - len([x for x in partition if x == 1])) <= ceil(n / 100)

    def enumerate_partitions(partition, depth, graph):
        if depth == len(graph):
            if check_valid_partition(partition, graph):
                return partition
            return None

        # Try assigning the current vertex to class 0
        partition[depth] = 0
        result = enumerate_partitions(partition, depth + 1, graph)
        if result is not None:
            return result

        # Try assigning the current vertex to class 1
        partition[depth] = 1
        result = enumerate_partitions(partition, depth + 1, graph)
        if result is not None:
            return result

        # If the current assignment failed, return None
        return None

    # Initialize the partition array with -1
    partition = [-1] * len(graph)
    # Call the enumeration function
    return enumerate_partitions(partition, 0, graph)



def partition_graphV2(graph):
    nb_nodes = graph.nb_nodes
    nb_edges = graph.nb_edges
    max_nodes_per_partition = ceil(nb_nodes/2) + floor(0.01 * nb_nodes)
    matrice_ponderation = calculate_weight_matrix(graph)
    min_node = min(graph.graphRep.keys())

    if min_node == 0:
        partition_1 = set(range(0, max_nodes_per_partition))
        partition_2 = set(range(max_nodes_per_partition, nb_nodes))
        sum_edge_weights = sum([matrice_ponderation[i][j] for i in partition_1 for j in partition_2])
    else:
        partition_1 = set(range(1, max_nodes_per_partition+1))
        partition_2 = set(range(max_nodes_per_partition+1, nb_nodes+1))
        sum_edge_weights = sum([matrice_ponderation[i-1][j-1] for i in partition_1 for j in partition_2])


    for _ in range(10):
        moved = True
        while moved:
            moved = False
            max_gain = 0
            best_i, best_j = None, None
            for i in partition_1:
                for j in partition_2:
                    if min_node == 0:
                        gain = matrice_ponderation[j][i] - matrice_ponderation[i][j]
                        if gain > max_gain:
                            max_gain = gain
                            best_i = i
                            best_j = j
                    else:
                        gain = matrice_ponderation[j-1][i-1] - matrice_ponderation[i-1][j-1]
                        if gain > max_gain:
                            max_gain = gain
                            best_i = i
                            best_j = j
            if max_gain > 0:
                partition_1.remove(best_i)
                partition_1.add(best_j)
                partition_2.remove(best_j)
                partition_2.add(best_i)
                sum_edge_weights -= max_gain
                moved = True

    if check_partitions(graph,partition_1,partition_2)!=True:
        print("NOT FEASIBLE")
        return

    return partition_1, partition_2, sum_edge_weights

def calculate_weight_matrix(graph):
    nb_nodes = graph.nb_nodes
    weight_matrix = [[0 for _ in range(nb_nodes)] for _ in range(nb_nodes)]
    min_node = min(graph.graphRep.keys())
    for i, edges in graph.graphRep.items():
        for j, weight in edges.items():
            weight_matrix[i - min_node][j] = weight
    return weight_matrix

def check_partitions(graph, partition_1, partition_2):
    nb_nodes = graph.nb_nodes
    min_node = min(graph.graphRep.keys())
    all_nodes = set(range(min_node, nb_nodes+min_node))

    # Vérifie que la somme des deux partitions correspond à tous les sommets du graphe
    if len(partition_1) + len(partition_2) != nb_nodes:
        return False

    # Vérifie que l'union des deux partitions est égale à l'ensemble de tous les sommets
    if partition_1.union(partition_2) != all_nodes:
        return False

    return True


def partition_graphV3(graph):
    def check_valid_partition(partition, Graphe):
        graph = Graphe.graphRep
        # Calculate the sum of weights between vertices in different classes
        sum_of_weights = 0
        n = len(graph)
        for i in graph:
            for j in graph[i]:
                if partition[i] != partition[j]:
                    if j in graph[i]:
                        sum_of_weights += graph[i][j]
        # Check if the sum of weights is minimal and the classes are roughly equally populated
        return sum_of_weights <= sum([sum(graph[i].values()) for i in graph]) and abs(
            len([x for x in partition if x == 0]) - len([x for x in partition if x == 1])) <= ceil(n / 100)

    def evaluate_partition(partition, Graphe):
        if check_valid_partition(partition, Graphe):
            # Calculate the sum of weights between vertices in different classes
            sum_of_weights = 0
            graph = Graphe.graphRep
            for i in graph:
                for j in graph[i]:
                    if partition[i] != partition[j]:
                        if j in graph[i]:
                            sum_of_weights += graph[i][j]
            return sum_of_weights
        else:
            # Return infinity if the partition is not valid
            return float('inf')

    # Define the number of partitions to generate
    p = 2
    n = len(graph)

    # Initialize the best partition and its score
    best_partition = None
    best_score = float('inf')

    # Generate all possible partitions
    for i in range(p**n):
        # Construct the i-th partition
        partition = [int(digit) for digit in format(i, f'0{n}b')]

        # Evaluate the partition
        score = evaluate_partition(partition, graph)

        # Update the best partition if necessary
        if score < best_score:
            best_partition = partition
            best_score = score

    return best_partition, best_score
