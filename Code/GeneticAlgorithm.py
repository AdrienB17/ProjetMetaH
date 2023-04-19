from math import ceil
import random
from ParseFile import *
from classGraph import *
from Gradient import estAreteInterclasse, computeCost, check_valid_partition


def initializePopulation(graph, pop_size):
    """
    Dans cette fonction on génère la population initiale qui va être utilisée comme
    point de départ dans l'algorithme génétique.
    Chaque individu est représenté par son codage binaire et sa note de fitness.
    Pour générer cette population on procède de la façon suivante :
        On tire aléatoirement une chaine de bits de longueur le nombre de noeuds du graphe.
        On vérifie que cette partition est bien valide au sens de l'équité.
        On calcule le score de fitness de cette partition valide.
        On continue jusqu'à atteindre POP_SIZE.
    """
    init_pop = []
    i = 0
    while (i < pop_size):
        ind = [random.randint(0, 1) for k in range(graph.nb_nodes)]
        isValid = check_valid_partition(ind, 0.10)
        #print(ind, isValid)
        if isValid : 
            cost = computeCost(graph, ind)
            init_pop.append((ind, cost))
            #print((ind, cost), sep="\n")
            i += 1
    return init_pop


def fortuneWheelSelection(pop , p:int) -> set:
    """ 
        On choisit p candidats parmi la population pop.
        Voir fonction random.choices du module random.
    """
    n = len(pop)
    sigma = sum(cost for (ind, cost) in pop)
    #print(sigma)
    S = []
    for j in range(p):
        k = 0
        x = random.randrange(sigma)
        #print(x)
        y = sigma
        i = 0
        while i < n and y > x:
            _, cost = pop[i]
            y = y - cost 
            k = i
            i += 1
        ind, cost = pop[k]
        S.append((ind, cost))
        #print(pop[k], sep="\n")
    return S

def tournament(individuals, s = 2):
    n = len(individuals)
    nb_comp = n//2
    while (len(individuals) != 1):
        pass

def tournamentSelection(partition, pop, s=2, p=0.7):
    """
        Le paramètre pop correspond à la population désirée, sélectionée après autant de tournois.
        Le paramètre s correspond à la taille du tournoi, par défaut il vaut 2.
            s doit être une puissance de 2.
        Le paramètre p correspond au taux d'acceptation du meilleur dans le tournoi.
            Cela signifie que le vainqueur d'un tournoi est pris dans la population retournée avec une probabilité de p.
            0.5 < p <= 1
            cf. "A Comparative Analysis of Selection Schemes Used in Genetic Algorithms", Goldberg & Deb
    """
    pass

def crossOver(partition1:list, partition2:list, N:int):
    crossPoint = random.randrange(N)    # On prend un point de croisement au hasard.
    #print(crossPoint)
    child1 = partition1[:crossPoint] + partition2[crossPoint:]
    child2 = partition2[:crossPoint] + partition1[crossPoint:]
    #print(child1)
    #print(child2)
    return child1, child2

def mutation(graph, pop:list, N:int, p = 0.001):
    for k in range(len(pop)) :
        mut = random.randrange(int(1/p))
        if (mut == 0) :
            mutationPoint = random.randrange(N)
            ind, cost = pop[k]
            ind[mutationPoint] = 1-ind[mutationPoint]
            cost = computeCost(graph, ind)
            pop[k] = ind, cost
    return pop

def bestInPop(pop):
    bestind = []
    min = 10000000
    for ind, cost in pop :
        if cost < min : 
            bestind = ind
            min = cost
    return (bestind, min)
        

def geneticAlgorithm(graph):
    pop_size = 128 # pop_size doit être une puissance de 2 pour l'instant.
    NB_GEN = 100
    N = graph.nb_nodes
    population = initializePopulation(graph, pop_size)
    #print(population)
    t = 0
    while (t < NB_GEN):
        t += 1
        print(f"Itération {t}")
        new_pop = fortuneWheelSelection(population, pop_size//2)
        for p in range(0, pop_size//2-1, 2):
            p1, c1 = new_pop[p]
            p2, c2 = new_pop[p+1]
            child1, child2 = crossOver(p1, p2, N)
            cout1 = computeCost(graph, child1)
            cout2 = computeCost(graph, child2)
            new_pop.append((child1, cout1))
            new_pop.append((child2, cout2))
        mutation(graph, new_pop, N, p = 0.001)
        population = new_pop
    
    print("Meilleure partition trouvée : ")
    print(bestInPop(population))
    #print(population)
    return population


## EXECUTION 
relative_path = "Code/samples/centSommets.txt"
graph = parse_file(relative_path)


pop = geneticAlgorithm(graph)