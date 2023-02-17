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
    return (res and partition[u] != partition[v])

def computeCost(graph, partition):
    '''
        Calcule le coût d'une partition (càd la somme du poids des arêtes interclasses)
    '''
    cost = 0
    for k in range(graph.nb_nodes):
        for l in range(graph.nb_nodes):
            if estAreteInterclasse(graph, (k,l), partition):
                cost += graph[k][l]
    return cost

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

def neighbourhoodPnD(graph, partition):
    '''
        Debug.
        Cette fonction renvoie le voisinage d'une configuraion donnée.
        mouvement élémentaire = PnD
    '''
    nbVois = 0
    nb0 = 0
    nb1 = 0
    for k in partition :
        if k : nb1 += 1
        else : nb0 += 1
    
    for k in range(len(partition)):
        cp_part = copy.deepcopy(partition)
        if (partition[k] == 0):
            cp_part[k] = 1-partition[k]
            nbVois += 1    
        elif (partition[k] == 1):
            cp_part[k] = 1-partition[k]
            nbVois += 1
        print(f'{k} : {str(partition)} -> {str(cp_part)}' )
    # On doit avoir nbVois = nb0 * nb1
    print(nbVois)
    print(nb0, nb1)

def argbestPnD(graph, partition, costPartition):
    '''
        Cherche dans le voisinge de la configuration "partition" le meilleur voisin (au sens du côut).
        mouvement élémentaire = Pick'n'Drop
        Renvoie un tuple comprenant :   best = la meilleure partition trouvée
                                        bestCost = le coût associé à best
                                        classSizes = le nombre de sommets dans chaque classe
    '''
    best = partition
    bestCost = costPartition
    classSizes = [0, 0]
    ## On calcule la taille des classes initiales
    for k in partition:
        if k == 0: classSizes[0] += 1
        else : classSizes[1] += 1

    # Dans ce cas, on inspecte tout le voisinage d'une configuration donnée.
    # Il y a n*(k-1) voisins avec ici k = 2 et n = le nombre de sommets du graphe.
    for k in range(graph.nb_nodes):
        cost = costPartition
        cp_part = copy.deepcopy(partition)
        if (partition[k] == 0):
            cp_part[k] = 1-partition[k]
            classSizes[0] -= 1
            classSizes[1] += 1
            #for l,v in graph[k].items():
            #    if partition[k] != partition[l] : cost -= v
        elif (partition[k] == 1):
            cp_part[k] = 1-partition[k]
            classSizes[1] -= 1
            classSizes[0] += 1
            #for l,v in graph[k].items():
            #    if partition[k] != partition[l] : cost -= v
        ## Ici le calcul du coût pose problème, trop lent O(n^2)
        cost = computeCost(graph, cp_part)
        #cost = int(random.random()*2000 % 2000)
        if (cost < bestCost and abs(classSizes[0]-classSizes[1]) <= 4):
            bestCost = cost
            best = cp_part
    return(best, bestCost, classSizes)


def gradient(graph):
    # C0 la configuration initiale par tirage aléatoire
    C0 = [random.randint(0, 1) for k in range(graph.nb_nodes)]
    # Calcul du coût de la solution initiale
    initCost = computeCost(graph, C0)
    print(f'Partition initiale : {str(C0)}\nCoût initial : {initCost}')

    Ci = C0
    costCi = initCost
    classSizes = []
    i = 1
    done = False
    #argbestSwap(graph, C0, 0)
    while (not done) :
        # neighbourhoodPnD(graph, C0)
        (Cip1, costCip1, classSz) = argbestPnD(graph, Ci, costCi)
        print(f'Itération {i} : Partition : {str(Cip1)} -- Coût : {costCip1}')
        if ( costCip1 < costCi ):
            i += 1
            Ci = Cip1
            costCi = costCip1
            classSizes = classSz
        else :
            done = True
    return (Ci, costCi, classSizes)