import copy
from math import ceil


def estAreteInterclasse(graph, edge, partition) -> bool:
    """
        Si le sommet u est dans une partition et v dans une autre alors l'arête est une arête interclasse.
    """
    res = 1
    u, v = edge
    # on vérifie que l'arête est bien dans le graphe
    try:
        graph[u][v]
    except KeyError:
        res = 0
    return (res and partition[u] != partition[v])


def compute_cost(graph, partition):
    """
        ReCalcule le coût d'une partition (càd la somme du poids des arêtes interclasses)
    """
    cost = 0
    for i in range(graph.nb_nodes):
        for j in range(i, graph.nb_nodes):
            if estAreteInterclasse(graph, (i, j), partition):
                cost += graph[i][j]
    return cost


class Solution:
    def __init__(self, partition, cost):
        self.partition = partition
        self.cost = cost
        self.classSizes = [len(partition) - sum(partition), sum(partition)]

    def is_valid(self, p):
        """
            Verifie que la partition est valide au sens de l equite.
            0 < param < 1
        """
        return abs(self.classSizes[0] - self.classSizes[1]) <= ceil(len(self.partition) * p)

    def get_cost(self):
        """
            Retourne le cout de la solution.
        """
        return self.cost

    def is_valid_after_pick_and_drop(self, i, p):
        """
            Verifie que la partition est valide au sens de l equite.
            0 < param < 1
        """
        class_sizes = copy.deepcopy(self.classSizes)
        class_sizes[self.partition[i]] -= 1
        class_sizes[1 - self.partition[i]] += 1

        return abs(class_sizes[0] - class_sizes[1]) <= ceil(len(self.partition) * p)

    def is_valid_after_swap(self, i, j, p):
        """
            Verifie que la partition est valide au sens de l equite.
        """
        return self.is_valid(p)

    def get_cost_after_pick_and_drop(self, i, graph):
        """
            Retourne le cout de la solution apres un pick and drop du sommet i.
        """
        cost = self.cost
        for k, w in graph[i].items():
            if self.partition[k] == self.partition[i]:
                # on rajoute le poids de l arete puisque i et k seront dans des classes differentes
                cost += w
            else:
                # on enleve le poids de l arete puisque i et k seront dans la meme classe
                cost -= w
        return cost

    def get_cost_after_swap(self, i, j, graph):
        """
            Retourne le cout de la solution apres un swap.
        """
        if self.partition[i] == self.partition[j]:
            return self.cost
        else:
            cost = self.cost
            for k, w in graph[i].items():
                if k == j:
                    continue
                elif self.partition[k] == self.partition[i]:
                    # on rajoute le poids de l arete puisque i et k seront dans des classes differentes
                    cost += w
                else:
                    # on enleve le poids de l arete puisque i et k seront dans la meme classe
                    cost -= w
            for k, w in graph[j].items():
                if k == i:
                    continue
                elif self.partition[k] == self.partition[j]:
                    # on rajoute le poids de l arete puisque j et k seront dans des classes differentes
                    cost += w
                else:
                    # on enleve le poids de l arete puisque j et k seront dans la meme classe
                    cost -= w
            return cost

    def pick_and_drop(self, i, new_cost):
        """
            Effectue un pick and drop du sommet i.
        """
        self.classSizes[self.partition[i]] -= 1
        self.classSizes[1 - self.partition[i]] += 1
        self.partition[i] = 1 - self.partition[i]
        self.cost = new_cost

    def swap(self, i, j, new_cost):
        """
            Effectue un swap des sommets i et j.
        """
        class_i = self.partition[i]
        self.partition[i] = self.partition[j]
        self.partition[j] = class_i
        self.cost = new_cost

    def __str__(self):
        """
            Affiche la solution
        """
        p1 = f'Classe 1 : {[v for v in range(len(self.partition)) if self.partition[v] == 0]}'
        p2 = f'Classe 2 : {[v for v in range(len(self.partition)) if self.partition[v] == 1]}'
        return p1 + p2

    def __deepcopy__(self):
        s = Solution(copy.deepcopy(self.partition), self.cost)
        s.classSizes = copy.deepcopy(self.classSizes)
        return s
