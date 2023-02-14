from ParseFile import *
from GradientGlouton import *
import os
import sys

if __name__ == '__main__':

    #filename = "/huitSommets_1.txt"
    filename = "/RG_13_3.txt"
    filepath = os.path.abspath('./Data/graph_samples/samples') + filename

    #graph = Graph()
    graph = parse_file(filepath)
    print(graph)
    partition = gradient(graph)