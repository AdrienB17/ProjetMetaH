from Gradient import *
from Enumeration import *
from GeneticAlgorithm import *
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
                                    2 = algorithme génétique

        Ecriture d'une solution sous la forme définie par les données spécifiques renvoyées par l'algorithme.
        De la forme générale : nom;nbNoeuds;+spécifiques
    '''
    with open(filepath_results, "a") as f:

        header = ""
        if algo == 0 : 
            header = "filename; nbNodes; BestCost; duration; eqParam ; nbValidSolutions ; nbSolutions\n"
        elif algo == 1 :
            header = "filename; nbNodes; initCost; finalCost; duration; eqParam\n"
        elif algo == 2 : 
            header = "filename; nbNodes; bestCost; duration; eqParam\n" 
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
                    # On récupére les données spécifiques renvoyées par un algorithme donné.
                    if algo == 0 :
                        if graph.nb_nodes <= 15:
                            best_partition, best_score , nb_valid_solutions, duree = explicit_enumeration(graph, param)
                        else:
                            print("L'instance est trop grande pour être résolue par énumération")
                            best_partition, best_score , nb_valid_solutions, duree = None, None, None, None
                    elif algo == 1:
                        partition, initCost, finalCost, classSizes, equity = gradient(graph, param)
                    elif algo == 2:
                        POP_SIZE = 100
                        NB_GEN = 30
                        if graph.nb_nodes < 1000 :
                            bestInd, bestCost = geneticAlgorithm(graph, POP_SIZE, NB_GEN)

                    duree = time.time() - begin

                    # Enregistrement du nom de l'instance, de la solution et du temps de traitement dans le fichier et des données spécifiques à l'algorithme.
                    if algo == 0 : 
                        outStr = f"{file};{graph.nb_nodes};{best_score};{duree};{param};{nb_valid_solutions};{2**graph.nb_nodes}\n"
                    elif algo == 1 :
                         outStr = f"{file};{graph.nb_nodes};{initCost};{finalCost};{duree};{param}\n" 
                    elif algo == 2 : 
                         outStr = f"{file};{graph.nb_nodes};{bestCost};{duree};{param}\n" 
                    f.write(outStr)
                    print(f"############# Fin du fichier {file} ##############")

def runForParameters(filename, outfile, parameters:list, algo=1):
    """
        Cette fonction permet d'exécuter l'algorithme donné en prenant comme paramètre (d'équité ici) chaque élément de la liste de "parameters".
        On exécute cette algorithme 100 fois sur le même paramètre. 
        Cette fonction sert essentiellement à faire des statistiques sur les solutions en fonction des paramètres.
    """
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

    # 0 : énumération 
    # 1 : gradient
    # 2 : algorithme génétique
    ALGO = 1

    folderpath = "./Samples"
    algName = ""
    if ALGO == 0:
        algName = "enumeration"
    elif ALGO == 1:
        algName = "gradient"
    elif ALGO == 2:
        algName = "genetique"

    filepath_results = f"./Solutions/results_algo_{ALGO}.txt"

    #relative_path = "../Data/CG_25_4.txt"
    #outfile = "../Solutions/parameters.txt"

    #parameters = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.15, 0.20, 0.25]
    #graph = parse_file(relative_path)

    #runForParameters(path+relative_path, path+outfile, parameters, 1)
    #runGradient(graph, 0.08)
    runAllInstances(folderpath, filepath_results, ALGO)