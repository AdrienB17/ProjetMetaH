import ParseFile

if __name__ == '__main__':

    fileName = "deuxTriangles.txt"
    file_path = '../Data/graph_samples/samples/' + fileName
    graph = ParseFile.parse_file(file_path)
    toto = 0