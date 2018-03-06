import csv
import matplotlib.pyplot as plt
import networkx as nx
import GraphMetric
import copy
from random import shuffle
from random import randint


class TemporalGraph:
    fileName = ""

    maxTime = 0  # maximum timestamp
    insGraphs = {0: nx.empty_graph()}  # instant graphs (graph <value> at each time instant <key>)
    G2 = {0: nx.empty_graph()}
    G3star = {0: nx.empty_graph()}
    G3 = nx.Graph()
    aggGraph = nx.Graph()
    graphObj = nx.Graph()

    no1 = []
    no2 = []
    timeStamps = []
    shuffledNodes1 = []
    shuffledNodes2 = []


    seedNode = -1

    def __init__(self, fileName, maxTime=7375):
        print("initializing TemporalGraph object from file", fileName, "upto time", maxTime)
        # TODO check if file exists
        self.fileName = fileName
        self.maxTime = maxTime
        self.loadGraphs()

    # Load shuffled temporal network G2 (Part C)
    def loadShuffledGraphs(self):
        print("loading shuffled temporal graph")

        # shuffles the edges (node1-node2 couples) without changing the corresponding time stamps
        zippedNodes = list(zip(self.no1, self.no2))
        shuffle(zippedNodes)
        self.shuffledNodes1, self.shuffledNodes2 = zip(*zippedNodes)

        for timeIndex in range(1, self.maxTime + 1):
            self.G2[timeIndex] = nx.empty_graph()
            self.G3star[timeIndex] = nx.empty_graph()
        for row in range(len(self.no1)):
            self.G2[self.timeStamps[row]].add_edge(self.shuffledNodes1[row],
                                                          self.shuffledNodes2[row],
                                                          t=self.timeStamps[row])

            rndIndex = randint(0, len(zippedNodes)-1)
            rndEdge = zippedNodes[rndIndex]
            self.G3star[self.timeStamps[row]].add_edge(*rndEdge, t=self.timeStamps[row])

            # Only add edge to shuffled aggregated graph if it doesn't exist yet
            if not self.G3.has_edge(*rndEdge):
                self.G3.add_edge(*rndEdge, t=self.timeStamps[row])
        return self

    # Loads instant graphs and aggregated graph from data file.
    def loadGraphs(self):
        print("loading instant graphs and aggregated graph")
        for timeIndex in range(1, self.maxTime + 1):
            self.insGraphs[timeIndex] = nx.empty_graph()
        with open(self.fileName, 'r') as dataFile:
            dataObj = csv.reader(dataFile, delimiter='\t', quotechar='"')
            next(dataObj)  # skip first line
            for row in dataObj:
                self.no1.append(int(row[0]))
                self.no2.append(int(row[1]))
                self.timeStamps.append(int(row[2]))
                self.insGraphs[self.timeStamps[-1]].add_edge(self.no1[-1],
                                                             self.no2[-1],
                                                             t=self.timeStamps[-1])

                # Only add edge to aggregated graph if it doesn't exist yet
                if not self.aggGraph.has_edge(int(row[0]), int(row[1])):
                    self.aggGraph.add_edge(int(row[0]), int(row[1]), t=int(row[2]))
        return self

    def getAggregatedGraph(self):
        return self.aggGraph

    def getInstantGraphs(self):
        return self.insGraphs

    def getInstantGraph(self, time):
        return self.insGraphs[time]

    def getG2(self):
        return self.G2

    def getG3(self):
        return self.G3

    def getG3star(self):
        return self.G3star

    def getInfectionsOverTime(self, seedNode):
        # print("getting infections over time with seed node", seedNode)
        self.seedNode = seedNode

        infectedList = {}
        timeInfected80 = None
        infectedThreshold = 0.8 * self.aggGraph.number_of_nodes()

        # infectionGraph = self.insGraphs.copy()
        # BUG: both point to the same dictionary! https://stackoverflow.com/questions/2465921/how-to-copy-a-dictionary-and-only-edit-the-copy
        infectionGraph = copy.deepcopy(self.insGraphs)  # instantiate with instant graphs

        # add SEED NODE to instant graph at time=0. It is the only element of that graph.
        if not infectionGraph[0].has_node(seedNode):
            infectionGraph[0].add_node(seedNode)
        nx.set_node_attributes(infectionGraph[0], True, 'infected')  # infect seed node (value irrelevant)

        for t in range(0, self.maxTime):
            if not t == 0:
                # Stop if all nodes already infected
                if infectedList[t - 1] == self.aggGraph.number_of_nodes():
                    print("all nodes infected at timestamp", t - 1, "/", self.maxTime)
                    for i in range(t - 1, self.maxTime + 1):
                        infectedList[i] = infectedList[t - 1]
                    break

                # Copy already infected nodes from previous timestamp
                for infectedNode in nx.get_node_attributes(infectionGraph[t - 1], 'infected'):
                    # nx.set_node_attributes(infectionGraph[t], True, 'infected')
                    infectionGraph[t].add_node(infectedNode, infected=True)

            # Infect new nodes
            infectedNodes = nx.get_node_attributes(infectionGraph[t], 'infected')
            for infectedNode in infectedNodes:
                for susceptibleNode in infectionGraph[t].neighbors(
                        infectedNode):  # nx.all_neighbors(infectionGraph[t], infectedNode):
                    if not susceptibleNode in infectedNodes:
                        infectionGraph[t].add_node(susceptibleNode, infected=True)

            # Count infected nodes
            infectedList[t] = len(nx.get_node_attributes(infectionGraph[t], 'infected'))

            # Register when 80% of nodes have been infected
            if not timeInfected80 and infectedList[t] >= infectedThreshold:
                print("Node: ", seedNode, "infects the 80% at time ", t)
                timeInfected80 = t

            # If a node never infects the 80% of the graph, just set it to the worst possible value
            if t == self.maxTime - 1 and not timeInfected80:
                timeInfected80 = t

        return infectedList, timeInfected80

    #  Plot number of infections over time. If the argument is a single infectionList, that is
    #  plotted as a line. If it is a dict of infectionLists (keyed by the seedNode with value
    #  the infectionlist), the expected value and variance of all infectionLists are plotted
    #  instead.
    def plotInfectionsOverTime(self, infectionLists):
        print("plotting infections over time")
        fig, ax = GraphMetric.plot(infectionLists)
        ax.set(title="Infections over time (%d seed nodes)" % len(infectionLists), ylabel='infections')
        plt.show()


    def plotGraph(self, g):
        print("plotting graph")
        print(list(self.graphObj.edges()))

        plt.figure(figsize=(8, 8))
        nx.draw_networkx(g, pos=nx.circular_layout(g), node_size=5)
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()