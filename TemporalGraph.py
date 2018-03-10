import csv
import matplotlib.pyplot as plt
import networkx as nx
import GraphMetric
import copy
import pickle
from random import shuffle
from random import randint


class TemporalGraph:
    fileName = ""

    maxTime = 0  # maximum timestamp
    insGraphs = {0: nx.empty_graph()}  # instant graphs (graph <value> at each time instant <key>)
    G2 = {0: nx.empty_graph()}
    G3star = {0: nx.empty_graph()}
    G3 = {0: nx.empty_graph()}
    G3_agg = nx.Graph()
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
        addedNodes = [0] * (self.maxTime + 1)
        # how many nodes have been added at each timestamp
        print("loading shuffled temporal graph")

        # shuffles the edges (node1-node2 couples) without changing the corresponding time stamps
        zippedNodes = list(zip(self.no1, self.no2))
        shuffle(zippedNodes)
        self.shuffledNodes1, self.shuffledNodes2 = zip(*zippedNodes)

        # instantiate the empty time graphs
        for timeIndex in range(1, self.maxTime + 1):
            self.G2[timeIndex] = nx.empty_graph()
            self.G3star[timeIndex] = nx.empty_graph()
            self.G3[timeIndex] = nx.empty_graph()

        # add the shuffled edges to the graphs
        # keeping the previous timestamps
        for row_num in range(len(self.no1)):
            self.G2[self.timeStamps[row_num]].add_edge(self.shuffledNodes1[row_num],
                                                       self.shuffledNodes2[row_num],
                                                       t=self.timeStamps[row_num])

            rndIndex = randint(0, len(zippedNodes) - 1)
            rndEdge = zippedNodes[rndIndex]
            self.G3star[self.timeStamps[row_num]].add_edge(*rndEdge, t=self.timeStamps[row_num])

            # Only add edge to shuffled aggregated graph if it doesn't exist yet
            if not self.G3_agg.has_edge(*rndEdge):
                for node in rndEdge:
                    if not self.G3_agg.has_node(node):
                        addedNodes[self.timeStamps[row_num]] += 1
                self.G3_agg.add_edge(*rndEdge, t=self.timeStamps[row_num])
                # Register time when nodes are first connected by an edge

        return addedNodes

    # Loads instant graphs and aggregated graph from data file.
    def loadGraphs(self):
        addedNodes = [0] * (self.maxTime + 1)
        endReading = False
        print("loading instant graphs and aggregated graph")
        for timeIndex in range(1, self.maxTime + 1):
            self.insGraphs[timeIndex] = nx.empty_graph()
        with open(self.fileName, 'r') as dataFile:
            dataObj = csv.reader(dataFile, delimiter='\t', quotechar='"')
            next(dataObj)  # skip first line
            for row in dataObj:
                if not endReading:
                    nodeI, nodeJ, timeStamp = [int(i) for i in row]

                    # print("Loading graphs for timestamp %d / %d" % (timeStamp, self.maxTime))

                    # Skip line if outside the time limit
                    if timeStamp > self.maxTime:
                        endReading = True
                        continue

                    self.no1.append(nodeI)
                    self.no2.append(nodeJ)
                    self.timeStamps.append(timeStamp)
                    self.insGraphs[timeStamp].add_edge(nodeI, nodeJ, t=timeStamp)

                    # Only add edge to aggregated graph if it doesn't exist yet
                    if not self.aggGraph.has_edge(nodeI, nodeJ):
                        # Register time when nodes are first connected by an edge
                        for node in (nodeI, nodeJ):
                            if not self.aggGraph.has_node(node):
                                addedNodes[timeStamp] += 1
                                self.aggGraph.add_node(node, t=timeStamp)
                        # Register as "edge time" the time when the edge was first added
                        self.aggGraph.add_edge(nodeI, nodeJ, t=timeStamp)

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

    def getInfectionsOverTime(self, seedNode, tempGraph, aggrGraph, infectedPercentage=0.8):
        # print("getting infections over time with seed node", seedNode)
        self.seedNode = seedNode

        infectedList = {}
        timeInfected80 = None  # timestamp at which the 80% of the nodes is infected
        infectedThreshold = round(infectedPercentage * aggrGraph.number_of_nodes())
        infectionGraph = []
        infectionGraph.append(copy.deepcopy(tempGraph[0]))  # instantiate with instant graphs

        # add SEED NODE to instant graph at time=0. It is the only element of that graph.
        infectionGraph[0].add_node(seedNode)
        nx.set_node_attributes(infectionGraph[0], True, 'infected')  # infect seed node (value irrelevant)

        for t in range(0, self.maxTime):
            # if timeInfected80 is None:  # less than 80% of the nodes are infected yet
            if not t == 0:
                # copy new time graph
                infectionGraph.append(copy.deepcopy(tempGraph[t]))
                # Stop if all nodes already infected
                if infectedList[t - 1] == aggrGraph.number_of_nodes():
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
                # nx.all_neighbors(infectionGraph[t], infectedNode):
                for susceptibleNode in infectionGraph[t].neighbors(infectedNode):
                    if susceptibleNode not in infectedNodes:
                        infectionGraph[t].add_node(susceptibleNode, infected=True)

            # Count infected nodes
            infectedList[t] = len(nx.get_node_attributes(infectionGraph[t], 'infected'))

            # Register when 80% of nodes have been infected
            if timeInfected80 is None and infectedList[t] >= infectedThreshold:
                print("Node: ", seedNode, "infects the 80% at time ", t)
                timeInfected80 = t

            # If a node never infects the 80% of the graph, just set it to the worst possible value
            if t == self.maxTime - 1 and not timeInfected80:
                timeInfected80 = t

        return infectedList, timeInfected80

    def evaluateInfections(self, gAgg, gInsts, fileName, seedMax, writeNewFile=False):
        # the number of nodes IS NOT the index of the last node
        N = gAgg.number_of_nodes()
        infectionLists = {}
        infected80 = {}

        if writeNewFile:
            # Use each node as seed node to spread infection (question 9)
            seedNodesNumber = N + 1

            print("Getting infections over time for %d seed nodes" % (seedNodesNumber - 1))
            for i in range(1, seedMax + 1):
                # print("Getting infections over time with seed node %d / %d" % (i, seedNodesNumber - 1))
                if not gAgg.has_node(i):
                    continue
                seedNode = i
                infectionLists[seedNode], infected80[seedNode] = self.getInfectionsOverTime(seedNode, gInsts, gAgg)

            # Saving the objects:
            with open(fileName, 'wb') as f:  # Python 3: open(..., 'wb')
                print('Writing on file %s' % fileName)
                pickle.dump([infectionLists, infected80], f)
        else:
            try:
                # Getting back the objects:
                with open(fileName, 'rb') as f:  # Python 3: open(..., 'rb')
                    print('Reading from file %s' % fileName)
                    infectionLists, infected80 = pickle.load(f)
            except IOError:
                print('FATAL ERROR: The file with the infected list could not be found.')

        return infectionLists, infected80

    @staticmethod
    def plotInfectionsOverTime(infectionLists, graphName='G'):

        #  Plot number of infections over time. If the argument is a single infectionList, that is
        #  plotted as a line. If it is a dict of infectionLists (keyed by the seedNode with value
        #  the infectionlist), the expected value and variance of all infectionLists are plotted
        #  instead.

        print("plotting infections over time")
        fig, ax = GraphMetric.plot(infectionLists)
        ax.set(title="Infections over time (%d seed nodes), graph %s" % (len(infectionLists), graphName),
               ylabel='I(t)')
        plt.show()
        return

    def plotGraph(self, g):
        print("plotting graph")
        print(list(self.graphObj.edges()))

        plt.figure(figsize=(8, 8))
        nx.draw_networkx(g, pos=nx.circular_layout(g), node_size=5)
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()
