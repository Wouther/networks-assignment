import TemporalGraph as tg
import matplotlib.pyplot as plt
import GraphMetric as gm
import numpy as np

# INFLUENCE OF TEMPORAL NETWORK FEATURES ON INFORMATION SPREADING

graphName = 'G2_tris'
fileName = "infection_lists_%s.pkl" % graphName

# gData = tg.TemporalGraph("data/Data_Dummy.txt", 10)
gData = tg.TemporalGraph("data/Data_Highschool.txt")

# ## G2 has many more new nodes on the first timeStamps
listNewNodes = gData.loadGraphs()
listNewNodesShuffled = gData.loadShuffledGraphs(readAggregate=False)

a = gData.splitAggregate( gData.getAggregatedGraph() )
print(a)

# tempCut2 = listNewNodes[:gData.maxTime-7300]
# plt.bar(range(len(tempCut2)), tempCut2, align='center')
# plt.title('New nodes graph G2')
# # plt.xticks(range(len(temporalDegreeList)), list(temporalDegreeList.keys()))
# plt.show()


# # randomized temporal graphs: same edges as in Gdata, but timestamps are shuffled
# G2 = gData.getG2()
# # Timestamps are randomly reassigned to the edges.
# #  An edge can be assigned no time stamps, or multiple time stamps.
# G3star = gData.getG3star()
# # Aggregated graph based on G3star, built in the same way as the original aggregated graph.
# G3 = gData.getG3()

# # how come the two average temporal degree are different?
# # also, the randomized graph always shows lower temporal degree.
# # maybe it's because on the same timeStamp the same edge is assigned twice.
# deg1 = 0
# deg2 = 0
# for t in range(1, gData.maxTime + 1):
#     deg1 += np.mean([degree for key, degree in gData.getG2atTime(t).degree()]) / gData.maxTime
#     deg2 += np.mean([degree for key, degree in gData.getInstantGraph(t).degree()]) / gData.maxTime
# print('shuffled ', deg1)
# print('original ', deg2)

# gAggregate = gData.getAggregatedGraph()
# gInstantaneous = gData.getG2()
# g3_agg = gData.getG3agg()
# seedMax = max(gData.getG2agg().nodes().items())[0]
# N = gData.getG2agg().number_of_nodes()
#
# # average degree: np.mean( [d for n, d in g3_agg.degree()] )
# writeNewFile = True
# infectionLists, infected80 = gData.evaluateInfections(gData.getG2agg(), gData.getG2(), fileName, seedMax, writeNewFile)
#
# gData.plotInfectionsOverTime(infectionLists, graphName)

# temporalDegreeList = {}
# temporalDegreeList_uw = {}
#
# for n in range(1, gData.maxTime + 1):  # initialize
#     temporalDegreeList[n] = 0
#     temporalDegreeList_uw[n] = 0
#
# oldNeighbors = [[0] for n in range(0, seedMax + 1)]
#
# for t in range(1, gData.maxTime + 1):  # for each timestamp
#     thisGraph = gInstantaneous[t]
#     for n in range(1, seedMax):  # for each node
#         if not thisGraph.has_node(n):
#             continue
#         if thisGraph.degree(n) != 0:
#             for neighbor in thisGraph.neighbors(n):
#                 if neighbor not in oldNeighbors[n] and n not in oldNeighbors[neighbor]:
#                     oldNeighbors[n].append(neighbor)
#                     temporalDegreeList[t] += 1 / t
#                     temporalDegreeList_uw[t] += 1
#
# # print(np.mean(temporalDegreeList_uw.values()))
# shuff = sum(temporalDegreeList.values())
#
# tempCut = [temporalDegreeList[k] for k in sorted(temporalDegreeList.keys())[:gData.maxTime - 7300]]
#
# plt.bar(range(len(temporalDegreeList) - 7300), tempCut, align='center')
# plt.title('Shuffled graph G2')
# # plt.xticks(range(len(temporalDegreeList)), list(temporalDegreeList.keys()))
# plt.show()
#
# temporaLDegreeList_orig = {}
# for n in range(1, gData.maxTime + 1):  # initialize
#     temporaLDegreeList_orig[n] = 0
# oldNeighbors = [[0] for n in range(0, seedMax + 1)]
# for t in range(1, gData.maxTime + 1):  # for each timestamp
#     thisGraph = gData.getInstantGraph(t)
#     for n in range(1, seedMax):  # for each node
#         if not thisGraph.has_node(n):
#             continue
#         if thisGraph.degree(n) != 0:
#             for neighbor in thisGraph.neighbors(n):
#                 if neighbor not in oldNeighbors[n] and n not in oldNeighbors[neighbor]:
#                     oldNeighbors[n].append(neighbor)
#                     temporaLDegreeList_orig[t] += 1 / t
# # print(np.mean(temporaLDegreeList_orig.values()))
# old = sum(temporaLDegreeList_orig.values())
#
# tempCut_orig = [temporaLDegreeList_orig[k] for k in sorted(temporaLDegreeList_orig.keys())[:gData.maxTime - 7300]]
#
# plt.bar(range(len(temporaLDegreeList_orig) - 7300), tempCut_orig, align='center')
# # plt.xticks(range(len(temporalDegreeList)), list(temporalDegreeList.keys()))
# plt.title('Original graph Gdata')
#
# plt.show()
#
# print(shuff, old)
#
# # # Nodes ranked by influence when seed node (question 10)
# # R = gm.sortKeyByAscVal(infected80)
# # print("Nodes ranked by influence when seed node (possibly same influence):", R)
# #
# #
# # rRD, rRD2, rRC, rRB2, rRTD, rRTD2, rRTD3, rRTD4, rRTD5 = gm.evaluateMetrics(N, seedMax,gData.maxTime,
# #                                                                             R, gInstantaneous, gAggregate)
# #
# # fig, ax = gm.plotLine(rRD, lineLabel='degree')
# # # gm.plotLine(rRD2, fig, 'degree 2')
# # gm.plotLine(rRC, fig, 'clustering coefficient')
# # # gm.plotLine(rRC2, fig)
# # gm.plotLine(rRB2, fig, 'betweenness')
# # # gm.plotLine(rRTD, fig, 'temporal degree')
# # gm.plotLine(rRTD2, fig, 'Temporal degree')
# # # gm.plotLine(rRTD3, fig, 'temporal degree 1.5 linear weight')
# # gm.plotLine(rRTD4, fig, 'Only new nodes temporal degree')
# # # gm.plotLine(rRTD5, fig, 'new temporal degree linear weight')
# #
# # ax.set(title="Recognition rate for different top-fractions, N=%d" % N,
# #        ylabel='recognition rate',
# #        xlabel='top-fraction f')
# # ax.legend() # ('rRD', 'rRD2', 'rRC', 'rRB2', 'rRTD')
# # plt.show()

print("End of part C.")
