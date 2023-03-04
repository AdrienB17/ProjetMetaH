import sys
import time
from Code.ParseFile import parse_file
from Code.Gradient import check_valid_partition, computeCost, show_solution


def explicit_enumeration(graph, param):
    begin = time.time()

    # Define the number of partitions to generate
    p = 2
    n = len(graph)
    # Initialize the best partition and its score
    best_partition = None
    best_score = float('inf')
    # Generate all possible partitions
    nb_valid_solutions = 0
    coef = 10
    for i in range(p ** n):
        # Construct the i-th partition
        partition = [int(digit) for digit in format(i, f'0{n}b')]
        if not check_valid_partition(partition, param):
            continue
        nb_valid_solutions += 1
        # Evaluate the partition
        score = computeCost(graph, partition)

        # Update the best partition if necessary
        if score < best_score:
            best_partition = partition
            best_score = score
        if time.time() - begin:
            print(i, " solutions évaluées ==> nb solutions valides : ", nb_valid_solutions)
            coef *= 10
    duree = time.time() - begin

    return best_partition, best_score, nb_valid_solutions, duree


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage : python3 Enumeration.py <nom_fichier>")
        print("Exemple : python3 Enumeration.py ../Data/graph_samples/samples/huitSommets_1.txt")
        relative_path = "../Data/graph_samples/samples/vingtCinqSommets.txt"
    else:
        relative_path = args[0]
    graph = parse_file(relative_path)
    print("Nombre de sommets : ", graph.nb_nodes)
    print("Nombre d'arêtes : ", graph.nb_edges)
    best_partition, best_score, nb_valid_solutions, duree = explicit_enumeration(graph, 0.08)
    print("Nombre de solutions totales :", 2 ** graph.nb_nodes)
    print("Nombre de solutions valides :", nb_valid_solutions)
    print("Durée : ", duree)
    print("Meilleure partition : ", best_partition)
    print("Meilleur score : ", best_score)
    show_solution(best_partition)
