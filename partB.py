import TemporalGraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy
from operator import itemgetter
import GraphMetric

# gData = TemporalGraph.TemporalGraph("data/Data_Highschool.txt")
gData = TemporalGraph.TemporalGraph("data/Data_Dummy.txt", 10)

# gInst = gData.loadInstantGraphs()
# gAgg = gData.loadAggregatedGraph()

# f = plt.figure(figsize=(8, 8))
# pl = nx.draw_shell(gAgg, node_size=1, width=0.02)
# plt.show()
# f = plt.figure(figsize=(8, 8))
#
# for i in range(1,10):
#     f.clear();
#     pl = nx.draw_shell(gInst[i], node_size=5)
#     plt.show()
#
#
# Gt = graphData.getGraphAtTime(7595);
#
# print(Gt.number_of_edges())
# print(Gt.number_of_nodes())

N = gData.getAggregatedGraph().number_of_nodes()

# Use each node as seed node to spread infection (question 9)
infectionLists = {}
infected80     = {}
for i in range(1,N+1):
    seedNode = i # numpy.random.randint(1,N+1)
    infectionLists[seedNode], infected80[seedNode] = gData.getInfectionsOverTime(seedNode)
gData.plotInfectionsOverTime(infectionLists)

# Nodes ranked by influence when seed node (question 10)
R = GraphMetric.sortKeyByAscVal(infected80)
print("Nodes ranked by influence when seed node (possibly same influence):", R)

# Nodes ranked by degree and clustering coefficient in aggregated graph (question 11)
degreeList     = {}
clusteringList = {}
for i in range(1,N+1):
    degreeList[i]     = gData.getAggregatedGraph().degree(i)
    clusteringList[i] = nx.clustering(gData.getAggregatedGraph(),i)
D = GraphMetric.sortKeyByDescVal(degreeList)
C = GraphMetric.sortKeyByDescVal(clusteringList)
print("Nodes ranked by degree (possibly same influence):", D)
print("Nodes ranked by clustering coefficient (possibly same influence):", C)



# infectionLists = {}
# seedNode = 5 # 213
# infectionLists[seedNode] = gData.getInfectionsOverTime(seedNode)
# gData.plotInfectionsOverTime(infectionLists)

print("done")
