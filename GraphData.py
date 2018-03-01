import csv
import matplotlib.pyplot as plt
import networkx as nx

class GraphData:
    fileName = ""
    graphObj = nx.Graph()

    def __init__(self, fileName):
        print("constructing new GraphData instance from file", fileName)
        self.loadFile(fileName)

    def loadFile(self, fileName):
        # TODO check if file exists and is valid csv file
        self.fileName = fileName

    def loadInstantGraphs(self):
        self.insGraphs = [];
        for timeIndex in range(0, 7375+1):
            self.insGraphs.append( nx.empty_graph() )
        with open(self.fileName, 'r') as dataFile:
            dbCSV = csv.reader(dataFile, delimiter='\t', quotechar='"')
            next(dbCSV)  # skip first line
            for row in dbCSV:
                self.insGraphs[ int(row[2])].add_edge(int(row[0]), int(row[1]), t=int(row[2]))
        return self.insGraphs
    
    def getAggregatedGraph(self):
        return self.graphAgg;

    def loadAggregatedGraph(self):
        self.graphAgg = nx.empty_graph();
        # TODO check if file exists and is valid csv file
        with open(self.fileName, 'r') as dataFile:
            dbCSV = csv.reader(dataFile, delimiter='\t', quotechar='"')
            next(dbCSV)  # skip first line
            for row in dbCSV:
                # If the two nodes were linked already, DO NOT add the new edge.
                if not self.graphAgg.has_edge(int(row[0]), int(row[1])):
                    self.graphAgg.add_edge(int(row[0]), int(row[1]), t=int(row[2]))
        return self.graphAgg

    # def instantGraph(self, time):
    #     self.instantGraph = nx.graph();
    #     next(self.fileName)  # skip first line
    #     for row in self.file:
    #         # If the edge was added at time t, add it to the graph
    #         if int(row[2]) == time:
    #             self.instantGraph.add_edge(int(row[0]), int(row[1]), t=int(row[2]))
    #     return self.instantGraph
    #
    #     # instantiate an empty graph
    #     instantGraph = nx.empty_graph();
    #     # Store all edges in a dictionary
    #     allEdges = nx.get_edge_attributes(self.graphObj, 't')
    #     for edge,currEdgeTime in allEdges.items():
    #         if currEdgeTime <= time: # add the edge if the link was made before time 't'
    #             instantGraph.add_edge(edge, currEdgeTime)
    #     return instantGraph

    def plotGraph(self):
        print("plotting graph")
        print(list(self.graphObj.edges()))

        plt.figure(figsize=(8, 8))
        nx.draw_networkx(self.graphObj, pos=nx.circular_layout(self.graphObj), node_size=5)
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()

    def plotGraphAgg(self):
        print("plotting graph")
        print(list(self.graphAgg.edges()))
        plt.figure(figsize=(8, 8))
        nx.draw_networkx(self.graphAgg, pos=nx.circular_layout(self.graphAgg), node_size=5)
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()

    def plotGraph(self, g):
        print("plotting graph")
        nx.draw_networkx(g, pos=nx.circular_layout(g), node_size=5)
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()