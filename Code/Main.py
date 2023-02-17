from ParseFile import *
from Gradient import *
from Enumeration import *
import os
import sys
import time

def runGradient(graph): 
    partition, cost, classSizes = gradient(graph)
    print(f'Partition trouvée : {partition} avec un coût de {cost}\nLa classe 0 possède {classSizes[0]} sommets et la classe 1 possède {classSizes[1]} sommets')

def runAllInstances(folderpath, outfile, algo=0):
    '''
        Exécute toutes les instances du dossier "folderpath" et écrit les résultats : file, sol, time
        dans le fichier outfile.
        Algorithme (défaut = 0) :   0 = énumération
                                    1 = gradient
    '''
    with open(filepath_results, "w") as f:
        # Boucle sur tous les fichiers du dossier
        files = os.listdir(folderpath)
        for file in files:
            # Si le fichier est un fichier texte
            if file.endswith(".txt"):
                path = folderpath+"/"+file
                graph = parse_file(path)
                if graph.nb_nodes <= 30:
                    # Mesurer le temps nécessaire pour trouver une solution
                    begin = time.time()
                    solution = partition_graphV3(graph)
                    duree = time.time() - begin

                    # Enregistrement du nom de l'instance, de la solution et du temps de traitement dans le fichier
                    f.write(f"Instance : {file}\n")
                    f.write(f"Solution : {solution}\n")
                    f.write(f"Temps de traitement : {duree} secondes\n\n")

if __name__ == '__main__':

    folderpath = "../Data/graph_samples/samples"
    filepath_results = "../Solutions/results.txt"

    relative_path = "/Data/graph_samples/samples/dixSeptSommets.txt"
    path = os.path.abspath("./")

    graph = parse_file(path + relative_path)
    print(graph)

    runGradient(graph)