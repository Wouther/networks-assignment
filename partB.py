import TemporalGraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import math
import GraphMetric as gm

gData = TemporalGraph.TemporalGraph("data/Data_Highschool.txt", 25)
# gData = TemporalGraph.TemporalGraph("data/Data_Dummy.txt", 10)

N = gData.getAggregatedGraph().number_of_nodes()

# Use each node as seed node to spread infection (question 9)
infectionLists = {}
infected80 = {}

seedNodesNumber = N+1
print("Getting infections over time for %d seed nodes" % (seedNodesNumber - 1))
for i in range(1, seedNodesNumber):
    # print("Getting infections over time with seed node %d / %d" % (i, seedNodesNumber - 1))
    if not gData.getAggregatedGraph().has_node(i):
        continue
    seedNode = i
    infectionLists[seedNode], infected80[seedNode] = gData.getInfectionsOverTime(seedNode)
# gData.plotInfectionsOverTime(infectionLists)

# Nodes ranked by influence when seed node (question 10)
R = gm.sortKeyByAscVal(infected80)
print("Nodes ranked by influence when seed node (possibly same influence):", R)

# Nodes ranked by degree and clustering coefficient in aggregated graph (question 11)
degreeList = {}
clusteringList = {}
for i in range(1, N + 1):
    if not gData.getAggregatedGraph().has_node(i):
        continue
    degreeList[i] = gData.getAggregatedGraph().degree(i)
    clusteringList[i] = nx.clustering(gData.getAggregatedGraph(), i)

# Nodes ranked by temporal metric: for each node, the weighted average of its degree for all timestamps,
# where the weights are the inverse temporal distance from the time the node was first connected to a graph.
temporalDegreeList = {}
for n in range(1, N + 1): # initialize
    temporalDegreeList[n] = 0
for t in range(1, gData.maxTime + 1): # for each timestamp
    thisGraph = gData.getInstantGraph(t)
    for n in range(1, N + 1): # for each node
        if not thisGraph.has_node(n):
            continue
        tDist = abs(t - gData.getAggregatedGraph().nodes[n]['t']) # temporal distance
        temporalDegreeList[n] += thisGraph.degree(n) / (tDist + 1)**2 # plus 1 to avoid division by zero

D  = gm.sortKeyByDescVal(degreeList)
D2 = gm.sortKeyByDescVal(nx.degree_centrality(gData.getAggregatedGraph()))
C  = gm.sortKeyByDescVal(clusteringList)
# C2 = gm.sortKeyByDescVal(nx.average_clustering(gData.getAggregatedGraph()))
B2 = gm.sortKeyByDescVal(nx.betweenness_centrality((gData.getAggregatedGraph())))
TD = gm.sortKeyByDescVal(temporalDegreeList)
print("Nodes ranked by degree (possibly same influence):", D)
print("\t(according to built-in function:", D2,")")
print("Nodes ranked by clustering coefficient (possibly same influence):", C)
# print("\t(according to built-in function:", C2,")")
print("Nodes ranked by betweenness (possibly same influence):")
print("\t(according to built-in function:", B2,")")
print("Nodes ranked by degree with temporal weights (possibly same influence):", TD)
print("\t(full list:", temporalDegreeList,")")

rRD = {} # influence / degree
rRD2 = {} # influence / degree
rRC = {} # influence / clustering coefficient
# rRC2 = {} # influence / clustering coefficient
rRB2 = {} # influence / node betweenness
rRTD = {} # influence / degree with temporal weights
for f in numpy.arange(0.05,0.55,0.05): # fraction ("top-f recognition rate")
    rRD[f] = gm.recognitionRate(f, R, D, N)
    rRD2[f] = gm.recognitionRate(f, R, D2, N)
    rRC[f] = gm.recognitionRate(f, R, C, N)
    # rRC2[f] = gm.recognitionRate(f, R, C2, N)
    rRB2[f] = gm.recognitionRate(f, R, B2, N)
    rRTD[f] = gm.recognitionRate(f, R, TD, N)

fig, ax = gm.plotLine(rRD)
gm.plotLine(rRD2, fig)
gm.plotLine(rRC, fig)
# gm.plotLine(rRC2, fig)
gm.plotLine(rRB2, fig)
gm.plotLine(rRTD, fig)
ax.set(title="Recognition rate for different top-fractions",
       ylabel='recognition rate',
       xlabel='top-fraction f')
ax.legend(('rRD', 'rRD2', 'rRC', 'rRB2', 'rRTD'))
plt.show()

print("End of part B.")
