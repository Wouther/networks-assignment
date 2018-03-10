import TemporalGraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy

print("initializing")
gData = TemporalGraph.TemporalGraph("data/Data_Highschool.txt")
# gData = TemporalGraph.TemporalGraph("data/Data_Dummy.txt", 10)
print("done")

G = gData.getAggregatedGraph()

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

degree_hist = nx.degree_histogram(G)
# format to be able to plot:
degree_hist_i = list(range(0, len(degree_hist)))
degree_hist_val = []
for i,val in enumerate(degree_hist):
    degree_hist_val.append(val)
sumVals = sum(degree_hist_val)
for i,val in enumerate(degree_hist_val):
    degree_hist_val[i] = val / sumVals # normalize

# histogram:
plt.hist(degree_sequence, len(degree_hist), normed=1, alpha=0.75)
ax = plt.gca()
ax.set(xlabel='degree k', ylabel='P(D=k)', title='Degree distribution of nodes')
ax.grid(which='both')
plt.show()

# scatterplot, regular axes:
# fig = plt.figure()
# ax = plt.gca()
# ax.plot(degree_hist_i, degree_hist_val, 'o', alpha=0.75, markeredgecolor='none')
# ax.set(xlabel='degree k', ylabel='P(D=k)', title='Degree distribution of nodes')
# ax.grid(which='both')
# plt.show()

# scatterplot, loglog axes:
fig = plt.figure()
ax = plt.gca()
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(degree_hist_i, degree_hist_val, 'o', alpha=0.75, markeredgecolor='none')
ax.set(xlabel='degree k', ylabel='P(D=k)', title='Degree distribution of nodes')
ax.grid(which='both')
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