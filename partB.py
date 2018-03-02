import TemporalGraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy

gData = TemporalGraph.TemporalGraph("data/Data_Highschool.txt")
# gData = GraphData.GraphData("data/Data_Dummy.txt", 10)

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

# infectionLists = {}
# for i in range(1,10):
#     seedNode = numpy.random.randint(1,gData.getAggregatedGraph().number_of_nodes()+1)
#     infectionLists[seedNode] = gData.getInfectionsOverTime(seedNode)
# gData.plotInfectionsOverTime(infectionLists)

infectionLists = {}
seedNode = 213
infectionLists[seedNode] = gData.getInfectionsOverTime(seedNode)
gData.plotInfectionsOverTime(infectionLists)

print("done")
