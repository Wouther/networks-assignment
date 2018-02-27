import csv
import networkx as nx


class GraphData:
    fileName = ""
    graphObj = nx.Graph()

    def __init__(self, fileName):
        print("constructing new GraphData instance from file", fileName)
        self.loadFile(fileName)
        # self.graphObj = nx.Graph()

    def loadFile(self, fileName):
        # TODO check if file exists and is valid csv file
        self.fileName = fileName
        with open(fileName, 'r') as dataFile:
            dbCSV = csv.reader(dataFile, delimiter='\t', quotechar='"')
            for row in dbCSV:
                # print(",", row)
                self.graphObj.add_node(row[0])
                self.graphObj.add_node(row[1])
                self.graphObj.add_edge(row[0], row[1], time=row[2])

        return True  # TODO don't always return true

    def plotGraph(self):
        print("plotting graph")
        print(list(self.graphObj.edges()))

        nx.draw_networkx(self.graphObj)

        plt.figure(figsize=(8, 8))
        # nx.draw_networkx_edges(G)
        # nx.draw_networkx_nodes(G,
        #                        node_size=80)
        #
        # plt.xlim(-0.05, 1.05)
        # plt.ylim(-0.05, 1.05)
        # plt.axis('off')
        # plt.show()

    def getGraphObj(self):
        return self.graphObj