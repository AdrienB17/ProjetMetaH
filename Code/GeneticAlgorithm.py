import random
from ParseFile import *
from classGraph import *
from Gradient import computeCost, check_valid_partition


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
        isValid = check_valid_partition(ind, 0.08)
        #print(ind, isValid)
        if isValid : 
            cost = computeCost(graph, ind)
            init_pop.append((ind, cost))
            #print((ind, cost), sep="\n")
            i += 1
    return init_pop


def fortuneWheelSelection(pop , p:int):
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
        x = random.randint(1, sigma)
        #print(x)
        y = sigma
        i = 0
        while i < n and x > y:
            _, cost = pop[i]
            y = y - cost 
            k = i
            i += 1
        ind, cost = pop[k]
        S.append((ind, cost))
        #print(pop[k], sep="\n")
    return S

def tournamentSelection(pop, p:int):
    """
        Séléction par tournoi, on fait s'affronter deux par deux au hasard les individus.
        L'individu avec le plus petit score de fitness (ici le poids des arêtes interclasse) est séléctionné.
        On continue jusqu'à atteindre une population de p individus.
        Attention, à chaque tournoi on ne retire pas de la population l'individu qui gagne, si bien
        qu'il peut être séléctionné plusieurs fois. Cependant si la population est assez grande, la probabilité d'être
        tiré plusieurs fois est très faible.
    """
    n = len(pop)
    S = []
    while (len(S) <= p):
        ind1, ind2 = random.sample(pop, 2)
        _, c1 = ind1
        _, c2 = ind2
        if (c1 < c2) : S.append(ind1)
        else : S.append(ind2)
    return S


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
        

def geneticAlgorithm(graph, popSize, nbGen):
    pop_size = popSize
    nb_gen = nbGen
    N = graph.nb_nodes
    population = initializePopulation(graph, pop_size)
    #print(population)
    t = 0
    while (t < nb_gen):
        t += 1
        print(f"Génération numéro {t}.")
        # On réduit la population de la génération précédente de moitié par séléction.
        #new_pop = fortuneWheelSelection(population, pop_size//2)
        new_pop = tournamentSelection(population, pop_size//2)
        # On prend deux individus dans la nouvelle populatione et on les fait se reproduire par crossOver.
        # Cette reproduction engendre 2 nouveaux individus qui sont ajoutés à la population.
        while (len(new_pop) < pop_size):
            parent1, parent2 = random.sample(population, 2)
            p1, c1 = parent1
            p2, c2 = parent2
            child1, child2 = crossOver(p1, p2, N)
            # Attention, on doit rejeter les partitions non-valides avec un taux proche de 1
            # sinon, on ne respecte plus le critère d'équité : c'est une sorte d'eugénisme.
            # On ne rejette pas tout les individus ne respectant pas ce critère pour conserver un brassage 
            # génétique et conserver le fait que toute configuration a une probabilité non nulle d'être vérifiée.
            # (même principe que la mutation).
            rejet = random.random()
            if check_valid_partition(child1, 0.08) or rejet > 0.90:
                cout1 = computeCost(graph, child1)
                new_pop.append((child1, cout1))
            if check_valid_partition(child2, 0.08) or rejet > 0.90:
                cout2 = computeCost(graph, child2)
                new_pop.append((child2, cout2))
        # On applique un facteur de mutation à la nouvelle population (probabilité de mutation de 1 pour 1000)
        mutation(graph, new_pop, N, p = 0.001)
        population = new_pop
    
    print("Meilleure partition trouvée : ")
    best = bestInPop(population)
    print(best)
    #print(population)

    # best est un tuple (bestInd:List, bestCost:float)
    return best


## EXECUTION 
relative_path = "Samples/centSommets.txt"
graph = parse_file(relative_path)

bestInd, bestCost = geneticAlgorithm(graph, 100, 30)
print(check_valid_partition(bestInd, 0.08))
