import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import GraphMetric

class TemporalGraph:
    fileName = ""

    maxTime = 0 # maximum timestamp
    N = 0 #number of nodes of the aggregated graph
    insGraphs = {} # instant graphs (graph <value> at each time instant <key>)
    aggGraph  = nx.Graph()
    graphObj = nx.Graph()

    seedNode   = -1
    infected80 = False

    def __init__(self, fileName, maxTime=7375):
        print("initializing TemporalGraph object from file", fileName, "upto time", maxTime)
        # TODO check if file exists
        self.fileName = fileName
        self.maxTime  = maxTime
        self.loadGraphs()

    # Loads instant graphs and aggregated graph from data file.
    def loadGraphs(self):
        print("loading instant graphs and aggregated graph")
        self.insGraphs = {0: nx.empty_graph()}
        self.aggGraph = nx.Graph()
        for timeIndex in range(1, self.maxTime+1):
            self.insGraphs[timeIndex] = nx.empty_graph()
        with open(self.fileName, 'r') as dataFile:
            dataObj = csv.reader(dataFile, delimiter='\t', quotechar='"')
            next(dataObj)  # skip first line
            for row in dataObj:
                self.insGraphs[int(row[2])].add_edge(int(row[0]), int(row[1]), t=int(row[2]))

                # Only add edge to aggregated graph if it doesn't exist yet
                if not self.aggGraph.has_edge(int(row[0]), int(row[1])):
                    self.aggGraph.add_edge(int(row[0]), int(row[1]), t=int(row[2]))
        self.N = self.aggGraph.number_of_nodes();
        return self
    
    def getAggregatedGraph(self):
        return self.aggGraph

    def getInstantGraphs(self):
        return self.insGraphs

    def getInstantGraph(self, time):
        return self.insGraphs[time]

    def getInfectionsOverTime(self, seedNode):
        print("getting infections over time with seed node", seedNode)
        self.seedNode = seedNode

        infectedList = {}

        infectionGraph = self.insGraphs.copy() # instantiate with instant graphs

        # Infect seed node
        if not infectionGraph[0].has_node(seedNode):
            infectionGraph[0].add_node(seedNode)
        nx.set_node_attributes(infectionGraph[0], True, 'infected') # infect seed node (value irrelevant)



        for t in range(0, self.maxTime):
            if t == 0 and self.infected80 == True:
                self.infected80 = False;

            if not t == 0:

                # Print the index if the 80% of the nodes have been infected
                infectedNumber = 0.8*self.N;
                if infectedList[t - 1] >= infectedNumber and self.infected80 == False:
                    print("80% of the nodes infected at time ", t-1)
                    self.infected80 = True

                # Stop if all nodes already infected
                if infectedList[t-1] == self.N:
                    print("all nodes infected at timestamp", t-1, "/", self.maxTime)
                    for i in range(t-1, self.maxTime + 1):
                        infectedList[i] = infectedList[t-1]
                    break

                # Copy already infected nodes from previous timestamp
                for infectedNode in nx.get_node_attributes(infectionGraph[t-1], 'infected'):
                    # nx.set_node_attributes(infectionGraph[t], True, 'infected')
                    infectionGraph[t].add_node(infectedNode, infected=True)

            # Infect new nodes
            infectedNodes = nx.get_node_attributes(infectionGraph[t], 'infected')
            for infectedNode in infectedNodes:
                for susceptibleNode in infectionGraph[t].neighbors(infectedNode): # nx.all_neighbors(infectionGraph[t], infectedNode):
                    if not susceptibleNode in infectedNodes:
                        infectionGraph[t].add_node(susceptibleNode, infected=True)

            # Count infected nodes
            infectedList[t] = len(nx.get_node_attributes(infectionGraph[t], 'infected'))

        return infectedList

    # Plot number of infections over time. If the argument is a single infectionList, that is
    #  plotted as a line. If it is a dict of infectionLists (keyed by the seedNode with value
    #  the infectionlist), the expected value and variance of all infectionLists are plotted
    #  instead.
    def plotInfectionsOverTime(self, infectionLists):
        print("plotting infections over time")
        fig, ax = GraphMetric.plot(infectionLists)
        ax.set(title="Infections over time (%d seed nodes)" % len(infectionLists), ylabel='infections')
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

    def plotGraphAgg(self):
        print("plotting graph")
        print(list(self.aggGraph.edges()))
        plt.figure(figsize=(8, 8))
        nx.draw_networkx(self.aggGraph, pos=nx.circular_layout(self.aggGraph), node_size=5)
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
