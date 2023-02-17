class Graph:
    def __init__(self, nb_nodes=0, nb_edges=0, deg_min=0, deg_max=0, graphRep={}, deg_nodes=[]):
        self.nb_nodes = nb_nodes
        self.nb_edges = nb_edges
        self.deg_min = deg_min
        self.deg_max = deg_max
        # grapheRep = représentation du graphe (dict de dict) 
        # clé : [(j1, c1), (j2, c2)...]
        self.graphRep = graphRep    
        self.deg_nodes = deg_nodes

    def __len__(self):
        return(self.nb_nodes)

    def __getitem__(self, key):
        return(self.graphRep[key])

    def __str__(self):
        st = f"Nombre de noeuds : {self.nb_nodes} \n"
        st += f"Nombre d'arêtes : {self.nb_edges} \n"
        st += f"(degMin : {self.deg_min}, degMax : {self.deg_max})\n"
        for k in self.graphRep:
            st += str(k) + ' : ' + str(self.graphRep[k]) + '\n'
        return st
