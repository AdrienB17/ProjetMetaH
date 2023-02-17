from ParseFile import *
from Gradient import *
from Enumeration import *
import os
import sys
import time

def runAllInstances(folderpath, outfile):
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
    #folderpath = "../DataTest"
    filepath_results = "../Solutions/results.txt"

    relative_path = "/"
    path = os.path.abspath("./")

    graph = parse_file(path + relative_path)
    print(graph)

    partition = gradient(graph)