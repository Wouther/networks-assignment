#__all__ = ['FinDB'] # list of submodules
import GraphData
import matplotlib.pyplot as plt
import networkx as nx
#from parser import *
###import FinDB

print("initializing")
graphData = GraphData.GraphData("data/Data_Highschool.txt")
# graphData.plotGraph()
print("done")

plt.figure(figsize=(10, 10))
# nx.draw_networkx_edges(G)
# nx.draw_networkx_nodes(G,
#                        node_size=80)
nx.draw(graphData.getGraphObj())

# plt.xlim(-0.05, 1.05)
# plt.ylim(-0.05, 1.05)
plt.axis('off')
plt.show()



