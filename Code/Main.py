from ParseFile import *
from Gradient import *
from Enumeration import *
import os
import sys
import time

def runGradient(graph): 
    partition, initCost, finalCost, classSizes, equity = gradient(graph)
    print(f'Partition trouvée : {partition} avec un coût de {finalCost}\nLa classe 0 possède {classSizes[0]} sommets et la classe 1 possède {classSizes[1]} sommets')
    cs = computeCost(graph, partition)
    print(f'Coût de la solution calculé par computeCost : {cs}\nEquilibre des classes : +- {equity} noeuds.')

def runAllInstances(folderpath, outfile, algo=1):
    '''
        Exécute toutes les instances du dossier "folderpath" et écrit les résultats : file, sol, time
        dans le fichier outfile.
        Algorithme (défaut = 0) :   0 = énumération
                                    1 = gradient
    '''
    with open(filepath_results, "a") as f:
        header = "filename; nbNodes; initCost; finalCost; duration\n"
        #outStr = ""
        f.write(header)
        # Boucle sur tous les fichiers du dossier
        files = os.listdir(folderpath)
        for file in files:
            # Si le fichier est un fichier texte
            if file.endswith(".txt"):
                path = folderpath+ "/" +file
                graph = parse_file(path)
                if graph.nb_nodes <= 500:
                    # Mesurer le temps nécessaire pour trouver une solution
                    print(f"############# Début du fichier {file} ##############")
                    begin = time.time()
                    if algo == 0 :
                        partition = partition_graphV3(graph)
                    elif algo == 1:
                        partition, initCost, finalCost, classSizes, equity = gradient(graph)
                    duree = time.time() - begin

                    # Enregistrement du nom de l'instance, de la solution et du temps de traitement dans le fichier
                    outStr = f"{file};{graph.nb_nodes};{initCost};{finalCost};{duree}\n"
                    f.write(outStr)
                    #f.write(f"Instance : {file}\n")
                    #f.write(f"Solution : {partition}\n")
                    #f.write(f"Temps de traitement : {duree} secondes\n\n")
                    print(f"############# Fin du fichier {file} ##############")
                    

if __name__ == '__main__':

    folderpath = "./Data/graph_samples/samples"
    filepath_results = "./Solutions/results.txt"

    relative_path = "/Data/graph_samples/samples/cinqSommets.txt"
    path = os.path.abspath("./")

    graph = parse_file(path + relative_path)

    #runGradient(graph)
    runAllInstances(folderpath, filepath_results, 1)