
from ParseFile import *
from classGraph import *
from Gradient import *
import os

def test_degrees(graph):
    '''
        On vérifie que les degrés donnés dans le fichier source correspondent 
        au nombre d'arcs que l'on créé pour chaque noeud.
    '''

def test_computeCost(graph):
    '''
        Test de la fonction de calcul du coût d'une solution.
        Ex: Pour une classe à un noeud et des poids de 1, on doit retrouver le degré du noeud.
    '''
    part = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    cost = computeCost(graph, part)
    print(cost)

if __name__ == '__main__':

    ## Importation des données
    folderpath = "../Data/graph_samples/samples"
    filepath_results = "../Solutions/results.txt"

    relative_path = "/Data/graph_samples/samples/dixSeptSommets.txt"
    path = os.path.abspath("./")

    graph = parse_file(path + relative_path)

    ## Tests
    test_computeCost(graph)