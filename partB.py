import GraphData
import matplotlib.pyplot as plt
import networkx as nx
import numpy

print("initializing")
graphData = GraphData.GraphData("data/Data_Highschool.txt")
print("done")

G = graphData.getGraphObj()

for i in range(1,10):
    Gt = graphData.getGraphAtTime(i)
    graphData.plotGraph(Gt)
    print(Gt.number_of_edges())
    print(Gt.number_of_nodes())

Gt = graphData.getGraphAtTime(7595);

print(Gt.number_of_edges())
print(Gt.number_of_nodes())

