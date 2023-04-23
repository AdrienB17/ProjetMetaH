import random

def calculate_gain(v, part1, part2, graph, p):
    # Taille des partitions au début
    part1_size = len(part1)
    part2_size = len(part2)

    # On déplace un noeud de part1 vers part2
    part2.setdefault(v, graph[v])
    del part1[v]

    # Taille des partitions après le mouvement
    new_part1_size = part1_size - 1
    new_part2_size = part2_size + 1

    # Vérification de la taille des partitions
    if abs(new_part1_size - new_part2_size) > p:
        # On déplace le noeud de part2 vers part1
        part1.setdefault(v, graph[v])
        del part2[v]

        # Le gain est défini à 0 si la taille est incorrecte
        return 0

    # Calcul du gain
    gain = new_part1_size - new_part2_size

    # Si le gain est inférieur à 0, alors on deplace le noeud de part2 vers part1
    if gain < 0:
        part1.setdefault(v, graph[v])
        del part2[v]

    return gain


def Kernighan_Lin(graph, p=None):
    nodes = list(graph.keys())
    n = len(nodes)

    # Partition initiale
    part1 = nodes[:n//2]
    part2 = nodes[n//2:]

    # Calcul de la coupe intiale
    cut = 0
    for node in part1:
        for neighbor, weight in graph[node].items():
            if neighbor in part2:
                cut += weight

    # On répète les opérations jusqu'à ce qu'il n'y ait plus d'amélioration possible.
    improvement = True
    while improvement:
        improvement = False
        best_gain = 0
        best_pair = None

        for i in range(n // 2):
            for j in range(n // 2, n):
                gain = calculate_gain(nodes[i], part1, part2, graph, p)

                if gain > best_gain:
                    best_gain = gain
                    best_pair = (nodes[i], nodes[j])

        if best_pair is not None:
            improvement = True
            node1, node2 = best_pair
            part1.remove(node1)
            part2.remove(node2)
            part1.append(node2)
            part2.append(node1)
            cut -= best_gain

    return part1, part2

