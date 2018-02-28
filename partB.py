import GraphData
import matplotlib.pyplot as plt
import networkx as nx
import numpy

print("initializing")
graphData = GraphData.GraphData("data/Data_Highschool.txt")
print("done")

G = graphData.getGraphObj()
print(G.number_of_edges())

Gt = graphData.getGraphAtTime(10)
print(Gt.number_of_edges())
