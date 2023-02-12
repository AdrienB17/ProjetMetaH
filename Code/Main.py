from ParseFile import *
import os
import sys

if __name__ == '__main__':

    filename = "/deuxTriangles.txt"
    filepath = os.path.abspath('./Data/graph_samples/samples') + filename

    #graph = Graph()
    graph = parse_file(filepath)
    #print(graphe.graph)
    print(graph)
    #toto = 0