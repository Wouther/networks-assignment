import GraphData
import matplotlib.pyplot as plt
import networkx as nx
import numpy

print("initializing")
gData = GraphData.GraphData("data/Data_Highschool.txt")
# print('loading instant graphs')
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

print('getting infections over time')
infectionList = gData.getInfectionsOverTime(150)
gData.plotInfectionsOverTime(infectionList)

print("done")
