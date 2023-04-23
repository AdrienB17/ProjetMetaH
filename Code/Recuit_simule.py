# solve graph partition problem using simulated annealing
# graph: graph to partition
# p: maximum size difference between partitions
# return: partition
import copy
import math
import sys
import time
from random import randint, choice

from Code.Enumeration import explicit_enumeration
#from Code.GeneticAlgorithm import geneticAlgorithm
#from Code.Gradient import check_valid_partition
from Code.ParseFile import parse_file
from Solution import Solution, compute_cost


def glouton_solution_version_1(graph, p=0.08):
    partition = [0 for _ in range(graph.nb_nodes)]
    class_sizes = [graph.nb_nodes, 0]
    # order edges by weight
    edges = []
    for i in range(graph.nb_nodes):
        for j, w in graph[i].items():
            edges.append((w, i, j))
    edges.sort(key=lambda x: x[0])

    while abs(class_sizes[0] - class_sizes[1]) > math.ceil(len(partition) * p) and len(edges) > 0:
        w, i, j = edges.pop()
        if partition[i] != partition[j] or partition[i] == 1:
            continue
        if partition[i] == 0:
            partition[j] = 1
            class_sizes[0] -= 1
            class_sizes[1] += 1

    if not abs(class_sizes[0] - class_sizes[1]) <= math.ceil(len(partition) * p):
        difference = abs(class_sizes[0] - class_sizes[1])
        biggest_class = 0 if class_sizes[0] > class_sizes[1] else 1
        biggest_class_items = [i for i in range(len(partition)) if partition[i] == biggest_class]
        for i in range(difference - math.ceil(len(partition) * p)):
            node = choice(biggest_class_items)
            partition[node] = 1 - partition[node]


    cost = compute_cost(graph, partition)

    return Solution(partition, cost)


def choose_neighbour(graph, x, p=0.08):
    node = randint(0, graph.nb_nodes - 1)
    if graph.nb_nodes%2 == 0 and math.ceil(graph.nb_nodes * p)==1:
        node2 = randint(0, graph.nb_nodes - 1)
        while node2 == node:
            node2 = randint(0, graph.nb_nodes - 1)
        x_neighbour = x.__deepcopy__()
        new_cost = x_neighbour.get_cost_after_swap(node, node2, graph)
        x_neighbour.swap(node, node2, new_cost)
        return x_neighbour
    else:
        while not x.is_valid_after_pick_and_drop(node, p):
            node = randint(0, graph.nb_nodes - 1)
        x_neighbour = x.__deepcopy__()
        new_cost = x_neighbour.get_cost_after_pick_and_drop(node, graph)
        x_neighbour.pick_and_drop(node, new_cost)
        return x_neighbour


def simulated_annealing(graph, max_iter_2, max_iter_1=10, p=0.08, T_0=100, T_min=0.01, mu=0.9,
                        initial_partition=glouton_solution_version_1):
    start_time = time.perf_counter()
    x = initial_partition(graph, p)
    print("solution initial : ", x.partition, " cost : ", compute_cost(graph, x.partition))
    x_best = x.__deepcopy__()
    f_min = x.get_cost()
    T = T_0
    t = 0
    while T > T_min and t < max_iter_1:
        #print(f'Itération {t} :  Coût : {x_best.get_cost()} -- {str(T)}')
        t_ = 0
        while t_ < max_iter_2:
            #print(f'      Itération {t} :  Coût : {x_best.get_cost()} -- {str(T)}')

            x_next = choose_neighbour(graph, x_best, p)
            if x_next.get_cost() != compute_cost(graph, x_next.partition):
                print("error :", x_next.partition, " ", x_next.get_cost(), " ", compute_cost(graph, x_next.partition))
            delta = x_next.get_cost() - x.get_cost()
            if delta < 0:
                x = x_next
                if x.get_cost() < f_min:
                    x_best = x.__deepcopy__()
                    f_min = x_next.get_cost()
                else:
                    t += 1
            else:
                if randint(0, 1) < math.exp(-delta / T):
                    x = x_next
            t_ += 1
        T *= mu

    return x_best, time.time() - start_time, t, T


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage : python3 Recuit_simule.py <nom_fichier>")
        print("Exemple : python3 Recuit_simule.py ../Samples/cinqSommets.txt")
        relative_path = "../Samples/centSommets.txt"
    else:
        relative_path = args[0]
    p = 0.08
    graph = parse_file(relative_path)
    print("Nombre de sommets : ", graph.nb_nodes)
    print("Nombre d'arêtes : ", graph.nb_edges)
    """
    best_partition, best_score, nb_valid_solutions, duree = explicit_enumeration(graph, p)
    print("Durée : ", duree)
    print("Meilleure partition : ", best_partition)
    print("Meilleur score : ", compute_cost(graph, best_partition))
    """
    print("simulated_annealing : ")
    solution, duree2, t, T = simulated_annealing(graph, min(graph.nb_edges, graph.nb_nodes))
    #print("Meilleure partition : ", solution.partition)
    print("Meilleur score : ", solution.get_cost())
    print(compute_cost(graph, solution.partition))
    print(solution.is_valid(p))
    solution, duree2, t, T = simulated_annealing(graph, (graph.nb_edges+graph.nb_nodes)*5)
    #print("Meilleure partition : ", solution.partition)
    print("Meilleur score : ", solution.get_cost())
    print(compute_cost(graph, solution.partition))
    print(solution.is_valid(p))

