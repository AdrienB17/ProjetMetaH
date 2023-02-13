import classGraph

def partition_graph(graph):
    def check_valid_partition(partition, graph):
        # Calculate the sum of weights between vertices in different classes
        sum_of_weights = 0
        for i in range(graph.nb_nodes):
            for j in range(i+1, graph.nb_nodes):
                if partition[i] != partition[j]:
                    if (i, j) in graph:
                        sum_of_weights += graph[(i, j)]
        # Check if the sum of weights is minimal and the classes are roughly equally populated
        return sum_of_weights <= graph.nb_edges and abs(len([x for x in partition if x == 0]) - len([x for x in partition if x == 1])) <= graph.nb_nodes//100

    def enumerate_partitions(partition, depth, graph):
        if depth == graph.nb_nodes:
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
    partition = [-1] * graph.nb_nodes
    # Call the enumeration function
    return enumerate_partitions(partition, 0, graph)