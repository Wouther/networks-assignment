import TemporalGraph as tg
import matplotlib.pyplot as plt
import GraphMetric as gm
import numpy as np

# INFLUENCE OF TEMPORAL NETWORK FEATURES ON INFORMATION SPREADING


writeNewFile = False
graphName = 'G2'
fileName = "infection_lists_%s.pkl" % graphName

# gData = TemporalGraph.TemporalGraph("data/Data_Dummy.txt", 10)
gData = tg.TemporalGraph("data/Data_Highschool.txt")
listNewNodes = gData.loadShuffledGraphs()

# # randomized temporal graphs: same edges as in Gdata, but timestamps are shuffled
# G2 = gData.getG2()
# # Timestamps are randomly reassigned to the edges.
# #  An edge can be assigned no time stamps, or multiple time stamps.
# G3star = gData.getG3star()
# # Aggregated graph based on G3star, built in the same way as the original aggregated graph.
# G3 = gData.getG3()

# gData.plotGraph(G3)
# histogram:

gAggregate = gData.getAggregatedGraph()
gInstantaneous = gData.getG2()

seedMax = max(gAggregate.nodes().items())[0]
N = gAggregate.number_of_nodes()

infectionLists, infected80 = gData.evaluateInfections(gAggregate, gInstantaneous, fileName, seedMax, writeNewFile)

gData.plotInfectionsOverTime(infectionLists, graphName)

# Nodes ranked by influence when seed node (question 10)
R = gm.sortKeyByAscVal(infected80)
print("Nodes ranked by influence when seed node (possibly same influence):", R)


rRD, rRD2, rRC, rRB2, rRTD, rRTD2, rRTD3, rRTD4, rRTD5 = gm.evaluateMetrics(N, seedMax,gData.maxTime,
                                                                            R, gInstantaneous, gAggregate)

fig, ax = gm.plotLine(rRD, lineLabel='degree')
# gm.plotLine(rRD2, fig, 'degree 2')
gm.plotLine(rRC, fig, 'clustering coefficient')
# gm.plotLine(rRC2, fig)
gm.plotLine(rRB2, fig, 'betweenness')
# gm.plotLine(rRTD, fig, 'temporal degree')
gm.plotLine(rRTD2, fig, 'Temporal degree')
# gm.plotLine(rRTD3, fig, 'temporal degree 1.5 linear weight')
gm.plotLine(rRTD4, fig, 'Only new nodes temporal degree')
# gm.plotLine(rRTD5, fig, 'new temporal degree linear weight')

ax.set(title="Recognition rate for different top-fractions, N=%d" % N,
       ylabel='recognition rate',
       xlabel='top-fraction f')
ax.legend() # ('rRD', 'rRD2', 'rRC', 'rRB2', 'rRTD')
plt.show()

print("End of part C.")