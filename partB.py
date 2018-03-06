import TemporalGraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import math
import GraphMetric as gm

# gData = TemporalGraph.TemporalGraph("data/Data_Highschool.txt")
gData = TemporalGraph.TemporalGraph("data/Data_Dummy.txt", 10)

N = gData.getAggregatedGraph().number_of_nodes()

# Use each node as seed node to spread infection (question 9)
infectionLists = {}
infected80 = {}

seedNodesNumber = N+1
# seedNodesNumber = 10
for i in range(1, seedNodesNumber):
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
    degreeList[i] = gData.getAggregatedGraph().degree(i)
    clusteringList[i] = nx.clustering(gData.getAggregatedGraph(), i)

D = gm.sortKeyByDescVal(degreeList)
C = gm.sortKeyByDescVal(clusteringList)
print("Nodes ranked by degree (possibly same influence):", D)
print("Nodes ranked by clustering coefficient (possibly same influence):", C)

rRD = {} # influence / degree
rRC = {} # influence / clustering coefficient
for f in numpy.arange(0.05,0.55,0.05): # fraction ("top-f recognition rate")
    rRD[f] = gm.recognitionRate(f, R, D, N)
    rRC[f] = gm.recognitionRate(f, R, C, N)
    print("recognition rate RD for f =", f, ":", rRD[f])
    print("recognition rate RC for f =", f, ":", rRC[f])

# fig, ax = gm.plotLine(rRD)
# fig, ax = gm.plotLine(rRC, fig)
# ax.set(title="Recognition rate for different top-fractions",
#        ylabel='recognition rate rRD/rRC',
#        xlabel='top-fraction f')
# ax.legend(('rRD', 'rRC'))
# plt.show()

# TODO implement 2 more features.
# My proposal:
# - average number of hops to go from 1 selected node to all the other nodes in the graph. (AGGREGATED)
# - betweenness of the selected node. (AGGREGATED)
# - also consider last line of the assignment when choosing the TEMPORAL FEATURE to implement

print("End of part B.")
