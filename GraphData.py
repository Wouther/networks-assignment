import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy

class GraphData:
    fileName = ""
    graphObj = nx.Graph()
    maxTime = 0
    insGraphs = []
    graphAgg = nx.Graph()

    def __init__(self, fileName, maxTime=7375):
        print("initializing GraphData object from file", fileName, "upto time", maxTime)
        # TODO check if file exists
        self.fileName = fileName
        self.maxTime  = maxTime

    def loadInstantGraphs(self):
        print("loading instant graphs")
        self.insGraphs = {0: nx.empty_graph()}
        for timeIndex in range(1, self.maxTime+1):
            self.insGraphs[timeIndex] = nx.empty_graph()
        with open(self.fileName, 'r') as dataFile:
            dbCSV = csv.reader(dataFile, delimiter='\t', quotechar='"')
            next(dbCSV)  # skip first line
            for row in dbCSV:
                self.insGraphs[int(row[2])].add_edge(int(row[0]), int(row[1]), t=int(row[2]))
        return self.insGraphs
    
    def getAggregatedGraph(self):
        return self.graphAgg

    def loadAggregatedGraph(self):
        print("loading aggregated graph")
        self.graphAgg = nx.empty_graph()
        # TODO check if file exists and is valid csv file
        with open(self.fileName, 'r') as dataFile:
            dbCSV = csv.reader(dataFile, delimiter='\t', quotechar='"')
            next(dbCSV)  # skip first line
            for row in dbCSV:
                # If the two nodes were linked already, DO NOT add the new edge.
                if not self.graphAgg.has_edge(int(row[0]), int(row[1])):
                    self.graphAgg.add_edge(int(row[0]), int(row[1]), t=int(row[2]))
        return self.graphAgg

    def getInstantGraphs(self, time):
        return self.insGraphs[time]

    def getInfectionsOverTime(self, seedNode):
        print("getting infections over time with seed node", seedNode)

        infectedList = {}

        if not self.graphAgg:
            self.loadAggregatedGraph()
        if not self.insGraphs:
            self.loadInstantGraphs()

        infectionGraph = self.insGraphs.copy() # instantiate with instant graphs

        # Infect seed node
        if not infectionGraph[0].has_node(seedNode):
            infectionGraph[0].add_node(seedNode)
        nx.set_node_attributes(infectionGraph[0], True, 'infected') # infect seed node (value irrelevant)

        for t in range(0, self.maxTime):
            if not t == 0:
                # Stop if all nodes already infected
                if infectedList[t-1] == self.graphAgg.number_of_nodes():
                    print("all nodes infected at timestep", t-1, "/", self.maxTime)
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
                    infectionGraph[t].add_node(susceptibleNode, infected=True)

            # Count infected nodes
            infectedList[t] = len(nx.get_node_attributes(infectionGraph[t], 'infected'))

        return infectedList

    # Plot number of infections over time. If the argument is a single infectionList, that is
    #  plotted as a line. If it is a dict of infectionLists (keyed by the seedNode with value
    #  the infectionlist), the expected value and variance of all infectionLists are plotted
    #  instead. [TODO implement]
    def plotInfectionsOverTime(self, infectionLists):
        print("plotting infections over time")
        fig, ax = plt.subplots()
        if not type(list(infectionLists.values())[0]) is dict:
            # Plot single line
            ax.plot(infectionLists.keys(), infectionLists.values())
        else:
            # Plot expectation and variance
            infectionListEnsemble = {}
            for seedNode,infectionList in infectionLists.items():
                for t,infections in infectionList.items():
                    if not t in infectionListEnsemble:
                        infectionListEnsemble[t] = []
                    infectionListEnsemble[t].append(infections)
            infectionListExpectation = {}
            infectionListStDev       = {}
            for t,infections in infectionListEnsemble.items():
                infectionListExpectation[t] = numpy.average(infections)
                infectionListStDev[t]       = numpy.sqrt(numpy.var(infections))
            ax.errorbar(infectionListExpectation.keys(), infectionListExpectation.values(),
                        yerr=infectionListStDev.values(), capsize=4)
        ax.set(xlabel='time [timestep]', ylabel='infections',
               title='Infections over time')
        ax.grid()
        # fig.savefig("output.png")
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