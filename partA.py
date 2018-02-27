import GraphData
import matplotlib.pyplot as plt
import networkx as nx
import numpy

print("initializing")
graphData = GraphData.GraphData("data/Data_Highschool.txt")
print("done")

G = graphData.getGraphObj()

N = G.number_of_nodes()
L = G.number_of_edges()
p = nx.density(G)
print("Number of nodes \tN =", N)
print("Number of links \tL =", L)
print("Link density    \tp =", p)  # p = E[L] / L_max = L / (N*(N-1)/2)

degree_sequence = [d for n, d in G.degree()]

# degree_distrib = nx.degree_histogram(G)
print("Average degree   \tE(D) =", numpy.average(degree_sequence))
print("Degree variance  \tVar(D) =", numpy.var(degree_sequence))

# n, bins, patches = plt.hist(d_hist)
n, bins, patches = plt.hist(degree_sequence, 50, normed=1, facecolor='green', alpha=0.75)
# plt.plot(range(1, len(degree_distrib) + 1), degree_distrib)
# l = plt.plot(bins, patches, 'r--', linewidth=1)
plt.show()

print("Degree assortativity  \trho_D =", nx.degree_assortativity_coefficient(G))

Cp = nx.average_clustering(G)
print("Clustering coefficient  \tC =", Cp)

Lp = nx.average_shortest_path_length(G)
print("Average hopcount  \tE[H] =", Lp)
print("Diameter  \tH_max =", nx.algorithms.distance_measures.diameter(G))

G_ER = nx.erdos_renyi_graph(G.number_of_nodes(), p)
L0 = nx.average_shortest_path_length(G_ER)
C0 = nx.average_clustering(G_ER)

print("Cp/C0 =", Cp / C0)
print("Lp/L0 =", Lp / L0)

print("Spectral radius \t\tlambda_1 =", max(abs(nx.adjacency_spectrum(G))))
print("Algebraic connectivity \ta = mu_{N-1} =", nx.algebraic_connectivity(G))
