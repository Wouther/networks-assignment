# Helper functions to manipulate data series from a TemporalGraph.
#
# One series is formatted as a dictionary keyed by timestamps. Multiple series are a dictionary of series keyed by some
# identifying value for the series (e.g. seed node) and the series itself as value.
import networkx as nx
import numpy
import matplotlib.pyplot as plt
from math import ceil


def isSingleSeries(series):
    return not type(list(series.values())[0]) is dict


# Calculate statistics across the different data series (ensemble), i.e. expected value and standard deviation.
def ensembleStatistics(series):
    if isSingleSeries(series):
        ensExp = series
        ensStdDev = dict.fromkeys(series, 0)
        ensMin = series
        ensMax = series
    else:
        # Combine all series into single one for easy processing
        seriesEnsemble = {}  # combine all series into single one
        for seriesId, thisSeries in series.items():
            for t, val in thisSeries.items():
                if not t in seriesEnsemble:
                    seriesEnsemble[t] = []
                seriesEnsemble[t].append(val)

        # Calculate expectation, standard deviation and minimum and maximum values
        ensExp = {}
        ensStdDev = {}
        ensMin = {}
        ensMax = {}
        for t, val in seriesEnsemble.items():
            ensExp[t] = numpy.average(val)
            ensStdDev[t] = numpy.sqrt(numpy.var(val))
            ensMin[t] = min(val)
            ensMax[t] = max(val)

    return ensExp, ensStdDev, ensMin, ensMax


# Plots single series as lines and ensembles of series as their expectation and variance. Optionally plot their range
#  (minimum and maximum values) instead.
def plot(series, minMax=False):
    if isSingleSeries(series):
        # Plot single line
        fig, ax = plotLine(series)
    elif not minMax:
        # Plot expectation and variance
        ensExp, ensStdDev = ensembleStatistics(series)[0:2]
        fig, ax = plotExpectationVariance(ensExp, ensStdDev)
    else:
        # Plot range
        ensMin, ensMax = ensembleStatistics(series)[2:4]
        fig, ax = plotMinMax(ensMin, ensMax)
    return fig, ax


def plotLine(series: object, fig: object = None, lineLabel=None) -> object:
    isNewFigure = not fig
    if isNewFigure:
        fig, ax = plt.subplots()
    else:
        ax = fig.get_axes()[0]

    # Plot single line
    plt.plot(series.keys(), series.values(), label=lineLabel, )

    if isNewFigure:
        ax.set(xlabel='time [timestamp]')
        ax.grid()
        # plt.show()
    return fig, ax


def plotExpectationVariance(ensExp, ensStdDev, fig=None):
    isNewFigure = not fig
    if isNewFigure:
        fig, ax = plt.subplots()
    else:
        ax = fig.get_axes()[0]  # TODO correct?

    # Plot expectation and variance
    errMinus = ensExp.copy()
    errPlus = ensExp.copy()
    for t in ensExp:
        errMinus[t] -= ensStdDev[t]
        errPlus[t] += ensStdDev[t]
    plt.plot(ensExp.keys(), ensExp.values())
    plt.fill_between(ensExp.keys(),
                     list(errMinus.values()), list(errPlus.values()),
                     facecolor='blue', alpha=0.15)

    if isNewFigure:
        ax.set(xlabel='time [timestamp]')
        ax.grid()
        # plt.show()
    return fig, ax


def plotMinMax(ensMin, ensMax, fig=None):
    isNewFigure = not fig
    if isNewFigure:
        newFigure = True
        fig, ax = plt.subplots()
    else:
        ax = fig.get_axes()[0]  # TODO correct?

    # Plot range (assumes keys are the same for min and max)
    plt.fill_between(ensMin.keys(),
                     list(ensMin.values()), list(ensMax.values()),
                     facecolor='blue', alpha=0.15)

    if isNewFigure:
        ax.set(xlabel='time [timestamp]')
        ax.grid()
        # plt.show()
    return fig, ax


# def drawGraph(series):
#     plt.figure(figsize=(8, 8))
#     nx.draw_networkx(self.graphObj, pos=nx.circular_layout(self.graphObj), node_size=5)
#     # nx.draw_networkx(g, pos=nx.circular_layout(g), node_size=5)
#     # plt.xlim(-0.05, 1.05)
#     # plt.ylim(-0.05, 1.05)
#     plt.axis('off')
#     plt.show()
#
# def drawGraphAgg(self):
#     print("plotting graph")
#     print(list(self.aggGraph.edges()))
#     plt.figure(figsize=(8, 8))
#     nx.draw_networkx(self.aggGraph, pos=nx.circular_layout(self.aggGraph), node_size=5)
#     # plt.xlim(-0.05, 1.05)
#     # plt.ylim(-0.05, 1.05)
#     plt.axis('off')
#     plt.show()

# Sorts a dictionaries values and returns a list of its keys in that sorted order.
# E.g. obtain a list of nodes sorted according to a metric.
def sortKeyByAscVal(series):
    return sorted(list(series.keys()), key=series.get)


def sortKeyByDescVal(series):
    return sorted(list(series.keys()), key=series.get, reverse=True)


# Nodes ranked by their recognition rate
# Nodes sharing a top ranking position in two metric sets
def recognitionRate(fraction, A, B, N):
    fN = ceil(N * fraction)
    Atop = A[0:fN + 1]
    Btop = B[0:fN + 1]
    return len(set(Atop) & set(Btop)) / fN


def degreeAndClustering(gAgg, seedMax):
    # Nodes ranked by degree and clustering coefficient in aggregated graph (question 11)
    degreeList = {}
    clusteringList = {}
    for i in range(1, seedMax):
        if not gAgg.has_node(i):
            continue
        degreeList[i] = gAgg.degree(i)
        clusteringList[i] = nx.clustering(gAgg, i)
    return degreeList, clusteringList


def evaluateMetrics(N, seedMax, maxTime, R, gInstantaneous, gAgg):
    # Nodes ranked by temporal metric: for each node, the weighted average of its degree for all timestamps,
    # where the weights are the inverse temporal distance from the time the node was first connected to a graph.
    temporalDegreeList = {}
    temporalDegreeList2 = {}
    temporalDegreeList3 = {}
    temporalDegreeList4 = {}
    temporalDegreeList5 = {}

    for n in range(1, seedMax):  # initialize
        temporalDegreeList[n] = 0
        temporalDegreeList2[n] = 0
        temporalDegreeList3[n] = 0
        temporalDegreeList4[n] = 0
        temporalDegreeList5[n] = 0

    oldNeighbors = [[0] for n in range(0, seedMax + 1)]

    for t in range(1, maxTime + 1):  # for each timestamp
        thisGraph = gInstantaneous[t]
        for n in range(1, seedMax):  # for each node
            if not thisGraph.has_node(n):
                continue

            # tDist = abs(t - gAgg.nodes[n]['t'])  # temporal distance since the first appearance
            # temporalDegreeList[n] += thisGraph.degree(n) / (tDist + 1) ** 2  # plus 1 to avoid division by zero
            temporalDegreeList2[n] += thisGraph.degree(n) / (t ** 2 + t)
            temporalDegreeList3[n] += thisGraph.degree(n) / t ** 1.5

            if thisGraph.degree(n) != 0:
                for neighbor in thisGraph.neighbors(n):
                    if neighbor not in oldNeighbors[n] and n not in oldNeighbors[neighbor]:
                        oldNeighbors[n].append(neighbor)
                        temporalDegreeList4[n] += 1 / t ** 2
                        temporalDegreeList5[n] += 1 / t

    # # Nodes ranked by degree and clustering coefficient in aggregated graph (question 11)
    degreeList, clusteringList = degreeAndClustering(gAgg, seedMax)

    D = sortKeyByDescVal(degreeList)
    D2 = sortKeyByDescVal(nx.degree_centrality(gAgg))
    C = sortKeyByDescVal(clusteringList)
    # C2 = sortKeyByDescVal(nx.average_clustering(gAgg))
    B2 = sortKeyByDescVal(nx.betweenness_centrality(gAgg))
    TD = sortKeyByDescVal(temporalDegreeList)
    TD2 = sortKeyByDescVal(temporalDegreeList2)
    TD3 = sortKeyByDescVal(temporalDegreeList3)
    TD4 = sortKeyByDescVal(temporalDegreeList4)
    TD5 = sortKeyByDescVal(temporalDegreeList5)
    print("Nodes ranked by degree (possibly same influence):", D)
    print("\t(according to built-in function:", D2, ")")
    print("Nodes ranked by clustering coefficient (possibly same influence):", C)
    # print("\t(according to built-in function:", C2,")")
    print("Nodes ranked by betweenness (possibly same influence):")
    print("\t(according to built-in function:", B2, ")")
    print("Nodes ranked by degree with temporal weights (possibly same influence):", TD)
    print("\t(full list:", temporalDegreeList, ")")

    rRD = {}  # influence / degree
    rRD2 = {}  # influence / degree
    rRC = {}  # influence / clustering coefficient
    # rRC2 = {} # influence / clustering coefficient
    rRB2 = {}  # influence / node betweenness
    rRTD = {}  # influence / degree with temporal weights
    rRTD2 = {}  # influence / degree with temporal weights
    rRTD3 = {}  # influence / degree with temporal weights
    rRTD4 = {}  # influence / degree with temporal weights
    rRTD5 = {}  # influence / degree with temporal weights

    for f in numpy.arange(0.05, 0.505, 0.005):  # fraction ("top-f recognition rate")
        rRD[f] = recognitionRate(f, R, D, N)
        rRD2[f] = recognitionRate(f, R, D2, N)
        rRC[f] = recognitionRate(f, R, C, N)
        # rRC2[f] = recognitionRate(f, R, C2, N)
        rRB2[f] = recognitionRate(f, R, B2, N)
        rRTD[f] = recognitionRate(f, R, TD, N)
        rRTD2[f] = recognitionRate(f, R, TD2, N)
        rRTD3[f] = recognitionRate(f, R, TD3, N)
        rRTD4[f] = recognitionRate(f, R, TD4, N)
        rRTD5[f] = recognitionRate(f, R, TD5, N)

    return rRD, rRD2, rRC, rRB2, rRTD, rRTD2, rRTD3, rRTD4, rRTD5
