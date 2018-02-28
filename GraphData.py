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
                # print(",", row)
                self.graphObj.add_node(row[0])
                self.graphObj.add_node(row[1])
                self.graphObj.add_edge(row[0], row[1], time=int(row[2]))

        return True  # TODO don't always return true

    def getGraphAtTime(self, t):
        # Initialize with empty graph (all nodes, no links)
        graphAtTime = self.graphObj.copy()
        graphAtTime.remove_edges_from(nx.edges(graphAtTime))

        # Add edges before time t
        edgesBeforeTime = nx.get_edge_attributes(graphAtTime, 'time') # get all edges with a 'time' attribute
        for edge in edgesBeforeTime.copy():
            if int(edgesBeforeTime[edge]) > t:
                # print(int(edgesAfterTime[edge]))
                del edgesBeforeTime[edge] # TODO does not work yet, only keeps a single edge (?!)
        graphAtTime.add_edges_from(edgesBeforeTime)

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

    def getGraphObj(self):
        return self.graphObj