import random
import classGraph
import copy

def estAreteInterclasse(graph, edge, partition) -> bool:
    '''
        Si le sommet u est dans une partition et v dans une autre alors l'arête est une arête interclasse
    '''
    res = 1
    u, v = edge
    ## on vérifie que l'arête est bien dans le graphe
    try:
        graph[u][v] 
    except KeyError :
        res = 0
    return (res and (partition[u] != partition[v]))

def swap(tab, a, b):
    tab[a], tab[b] = tab[b], tab[a]

def neighbourhoodSwap(graph, partition):
    '''
        Debug.
        Cette fonction renvoie le voisinage d'une configuraion donnée.
        mouvement élémentaire = swap
        nombre de voisins pour 2 classes n1*n2, n1 = card partition 1 et n2 = card partition 2
    '''
    nbVois = 0
    nb0 = 0
    nb1 = 0
    for k in partition :
        if k : nb1 += 1
        else : nb0 += 1
    
    for k in range(len(partition)):
        if (partition[k] == 0):
            for l in range(len(partition)):
                cp_part = copy.deepcopy(partition)
                if (partition[l] == 1):
                    swap(cp_part, k, l)
                    nbVois += 1
                    print(f'{k, l} : {str(partition)} -> {str(cp_part)}' )
    # On doit avoir nbVois = nb0 * nb1
    print(nbVois)
    print(nb0, nb1)

def argbestSwap(graph, partition, costPartition):
    best = []
    bestCost = costPartition
    for k in range(len(partition)):
        if (partition[k] == 0):
            for l in range(len(partition)):
                cost = costPartition
                cp_part = copy.deepcopy(partition)
                if (partition[l] == 1):
                    if estAreteInterclasse(graph, (l,k), partition):
                        #print(f'{l, k} Arête interclasse')
                        cost -= graph[l][k]
                    # Si les deux noeuds dont on a changé les classes forment une arête interclasse
                    # on modifie le côut de la solution
                    swap(cp_part, k, l)
                    cost += graph[k][l]
                    if cost < bestCost :
                        bestCost = cost
                        best = cp_part
    return (best, bestCost)

def computeCost(graph, partition):
    cost = 0
    for k in range(graph.nb_nodes):
        if partition[k] == 0:
            for l in range(graph.nb_nodes):
                if partition[l] == 1 and estAreteInterclasse(graph, (k,l), partition):
                    cost += graph[k][l]
    return cost

def gradient(graph):
    # C0 la configuration initiale par tirage aléatoire
    C0 = [random.randint(0, 1) for k in range(graph.nb_nodes)]
    # Calcul du coût de la solution initiale
    initCost = computeCost(graph, C0)
    print(f'Partition initiale : {str(C0)}\nCoût initial : {initCost}')

    Ci = C0
    costCi = initCost
    i = 0
    done = False
    #argbestSwap(graph, C0, 0)
    while (i < 4) :
        (Cip1, costCip1) = argbestSwap(graph, C0, costCi)
        print(f'Itération {i} : Partition : {str(Cip1)} -- Coût : {costCip1}')
        if ( costCip1 < costCi ):
            i += 1
            Ci = Cip1
            costCi = costCip1
        else :
            break
            done = True
    return Ci