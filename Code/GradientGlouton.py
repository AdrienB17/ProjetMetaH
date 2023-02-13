import random
import classGraph

def estAreteInterclasse(arete, partition) -> bool:
    ## Si le sommet u est dans une partition et v dans une autre alors l'arête est une arête interclasse
    u, v = arete
    return partition[u] != partition[v] 

def gradient_glouton(graph):
    cost = 0
    # Initialisation avec une partition aléatoire
    partition = [ random.randint(0, 1) for k in range(graph.nb_nodes)]

    while True:
        updated = False
        for u in graph.graphRep:
            for v, weight in graph[u]:
                if partition[u] == partition[v]:
                    continue
                new_cost = cost - 2 * weight  # en déplaçant le sommet de la partition
                if new_cost < cost:
                    partition[u] = 1 - partition[u]
                    cost = new_cost
                    updated = True
        if not updated:
            break

    return partition
