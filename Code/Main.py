from Gradient import *
from Enumeration import *
import os
import time

def runGradient(graph, param): 
    partition, initCost, finalCost, classSizes, equity = gradient(graph, param)
    print(f'Partition trouvée : {partition} avec un coût de {finalCost}\nLa classe 0 possède {classSizes[0]} sommets et la classe 1 possède {classSizes[1]} sommets')
    cs = computeCost(graph, partition)
    print(f'Coût de la solution calculé par computeCost : {cs}\nEquilibre des classes : +- {equity} noeuds.')

def runAllInstances(folderpath, outfile, algo=1):
    '''
        Exécute toutes les instances du dossier "folderpath" et écrit les résultats : file, sol, time
        dans le fichier outfile.
        Algorithme (défaut = 0) :   0 = énumération
                                    1 = gradient

        Ecriture d'une solution sous forme : "filename; nbNodes; initCost; finalCost; duration; eqParam"
            filename : le nom du fichier testé
            nbNodes : le nombre de sommets de l'instance
            initCost : le coût associé à la partition initiale
            finalCost : le coût trouvé à la fin de l'exécution
            duration : la durée d'exécution
            eqParam : le paramètre d'équité des classes de sorte que l'equité (en nombre de noeuds) soit égale à nbNodes*eqParam
    '''
    with open(filepath_results, "a") as f:
        header = "filename; nbNodes; initCost; finalCost; duration; eqParam\n" \
            if algo == 1 else "filename; nbNodes; BestCost; duration; eqParam ; nbValidSolutions ; nbSolutions\n"
        #outStr = ""
        f.write(header)
        # Boucle sur tous les fichiers du dossier
        files = os.listdir(folderpath)
        for file in files:
            # Si le fichier est un fichier texte
            if file.endswith(".txt"):
                path = folderpath+ "/" + file
                graph = parse_file(path)
                if graph.nb_nodes <= 1000:
                    # Mesurer le temps nécessaire pour trouver une solution
                    print(f"############# Début du fichier {file} ##############")
                    begin = time.time()
                    param = 0.08
                    if algo == 0 :
                        if graph.nb_nodes <= 15:
                            best_partition, best_score , nb_valid_solutions, duree = explicit_enumeration(graph, param)
                        else:
                            print("L'instance est trop grande pour être résolue par énumération")
                            best_partition, best_score , nb_valid_solutions, duree = None, None, None, None
                    elif algo == 1:
                        partition, initCost, finalCost, classSizes, equity = gradient(graph, param)
                    duree = time.time() - begin
                    # Enregistrement du nom de l'instance, de la solution et du temps de traitement dans le fichier
                    outStr = f"{file};{graph.nb_nodes};{initCost};{finalCost};{duree};{param}\n" \
                        if algo == 1 else f"{file};{graph.nb_nodes};{best_score};{duree};{param};{nb_valid_solutions};{2**graph.nb_nodes}\n"
                    f.write(outStr)
                    print(f"############# Fin du fichier {file} ##############")

def runForParameters(filename, outfile, parameters, algo=1):
    with open(outfile, "a") as f:
        header = "filename;nbNodes;initCost;finalCost;duration;param\n" \
            if algo == 1 else "filename; nbNodes; BestCost; duration; eqParam ; nbValidSolutions ; nbSolutions\n"
        f.write(header)

        graph = parse_file(filename)
        file = filename.split('/')[-1]

        for k in parameters:
            for i in range(100):
                begin = time.time()
                if algo == 0:
                    partition = explicit_enumeration(graph, k)
                elif algo == 1:
                    partition, initCost, finalCost, classSizes, equity = gradient(graph, k)
                duree = time.time() - begin

                # Enregistrement du nom de l'instance, de la solution et du temps de traitement dans le fichier
                outStr = f"{file};{graph.nb_nodes};{initCost};{finalCost};{duree};{k}\n"
                f.write(outStr)


if __name__ == '__main__':

    folderpath = "../Data/"
    filepath_results = "../Solutions/results.txt"

    relative_path = "../Data/CG_25_4.txt"
    outfile = "../Solutions/parameters.txt"

    parameters = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.15, 0.20, 0.25]
    graph = parse_file(relative_path)

    #runForParameters(path+relative_path, path+outfile, parameters, 1)
    #runGradient(graph, 0.08)
    runAllInstances(folderpath, filepath_results, 1)