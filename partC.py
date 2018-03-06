import TemporalGraph

# INFLUENCE OF TEMPORAL NETWORK FEATURES ON INFORMATION SPREADING

# gData = TemporalGraph.TemporalGraph("data/Data_Dummy.txt", 10)
gData = TemporalGraph.TemporalGraph("data/Data_Highschool.txt")

gData.loadShuffledGraphs()

# randomized temporal graphs: same edges as in Gdata, but timestamps are shuffled
G2 = gData.getG2()

# Timestamps are randomly reassigned to the edges.
#  An edge can be assigned no time stamps, or multiple time stamps.
G3star = gData.getG3star()

# Aggregated graph based on G3star, built in the same way as the original aggregated graph.
G3 = gData.getG3()

# redesigned plotGraph function
gData.plotGraph(G3)

# TODO perform on G2,G3 the processes described in part B.



print("End of part C.")