import random
from math import ceil
import copy

import random

import random
from math import ceil
import copy

import random

def calculate_gain(v, part1, part2, graph, p):
    # Size of partitions before movement
    part1_size = len(part1)
    part2_size = len(part2)

    # Move the node from part1 to part2
    part2.setdefault(v, graph[v])
    del part1[v]

    # Size of partitions after the movement
    new_part1_size = part1_size - 1
    new_part2_size = part2_size + 1

    # We verify that the partitions size are correct
    if abs(new_part1_size - new_part2_size) > p:
        # Move node from part2 to part1
        part1.setdefault(v, graph[v])
        del part2[v]

        # Gain = 0 because size incorrect
        return 0

    # Calcul of the gain
    gain = new_part1_size - new_part2_size

    # Move node from part2 to part1 if gain < 0
    if gain < 0:
        part1.setdefault(v, graph[v])
        del part2[v]

    return gain


def Kernighan_Lin(graph, p=None):
    nodes = list(graph.keys())
    n = len(nodes)

    # initial partition
    part1 = nodes[:n//2]
    part2 = nodes[n//2:]

    # calculate initial cut
    cut = 0
    for node in part1:
        for neighbor, weight in graph[node].items():
            if neighbor in part2:
                cut += weight

    # repeat until no further improvement possible
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

