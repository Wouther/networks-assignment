import pathpy
import csv

# Load data from file into graph object
G = pathpy.TemporalNetwork()
with open("data/Data_Highschool.txt", 'r') as dataFile:
    dataCSV = csv.reader(dataFile, delimiter='\t', quotechar='"')
    next(dataCSV)  # skip first line
    for row in dataCSV:
        G.addEdge(row[0], row[1], row[2])
        G.addEdge(row[1], row[0], row[2]) # also v.v. for undirected edge
        print(G.vcount())

# print(G.vcount())
