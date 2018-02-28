import csv
import matplotlib.pyplot as plt
import networkx as nx

class GraphData:
    fileName = ""
    graphObj = nx.Graph()

    def __init__(self, fileName):
        print("constructing new GraphData instance from file", fileName)
        self.loadFile(fileName)
        # self.graphObj = nx.Graph()

    def loadFile(self, fileName):
        # TODO check if file exists and is valid csv file
        self.fileName = fileName
        with open(fileName, 'r') as dataFile:
            dbCSV = csv.reader(dataFile, delimiter='\t', quotechar='"')
            next(dbCSV) # skip first line
            for row in dbCSV:
                # If the two nodes were linked already, DO NOT add the new edge.
                if not self.graphObj.has_edge(int(row[0]),  int(row[1])):
                    self.graphObj.add_edge(int(row[0]), int(row[1]), t=int(row[2]))
        return True  # TODO don't always return true

    def getGraphAtTime(self, time):
        # Initialize with empty graph (all nodes, no links)
        graphAtTime = nx.empty_graph();
        # Store all edges in a dictionary
        allEdges = nx.get_edge_attributes(self.graphObj, 't')
        for edge,currEdgeTime in allEdges.items():
            if currEdgeTime <= time: # add the edge if the link was made before time 't'
                graphAtTime.add_edge(edge, currEdgeTime)
        return graphAtTime

    def plotGraph(self):
        print("plotting graph")
        print(list(self.graphObj.edges()))

        plt.figure(figsize=(8, 8))
        nx.draw_networkx(self.graphObj, pos=nx.circular_layout(self.graphObj), node_size=5)
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()

    def plotGraph(self):
        print("plotting graph")
        print(list(self.graphObj.edges()))

        plt.figure(figsize=(8, 8))
        nx.draw_networkx(self.graphObj, pos=nx.circular_layout(self.graphObj), node_size=5)
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()

    def plotGraph(self, g):
        print("plotting graph")
        plt.figure(figsize=(8, 8))
        nx.draw_networkx(g, pos=nx.circular_layout(g), node_size=5)
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()

    def getGraphObj(self):
        return self.graphObj