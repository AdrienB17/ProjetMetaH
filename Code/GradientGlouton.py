import random
import Data


def gradient_glouton(graph):
    cost = 0
    partitions = [0] * graph.nb_nodes  # initialiser les partitions de manière aléatoire
    for i in range(graph.nb_nodes):
        partitions[i] = random.randint(0, 1)

    while True:
        updated = False
        for u in graph.graph:
            for v, weight in graph.graph[u]:
                if partitions[u] == partitions[v]:
                    continue
                new_cost = cost - 2 * weight  # en déplaçant le sommet de la partition
                if new_cost < cost:
                    partitions[u] = 1 - partitions[u]
                    cost = new_cost
                    updated = True
        if not updated:
            break

    return partitions
