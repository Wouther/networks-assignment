# Helper functions to manipulate data series from a TemporalGraph.
#
# One series is formatted as a dictionary keyed by timestamps. Multiple series are a dictionary of series keyed by some
# identifying value for the series (e.g. seed node) and the series itself as value.

import numpy
import matplotlib.pyplot as plt

def isSingleSeries(series):
    return not type(list(series.values())[0]) is dict

# Calculate statistics across the different data series (ensemble), i.e. expected value and standard deviation.
def ensembleStatistics(series):
    if isSingleSeries(series):
        ensExp    = series
        ensStdDev = dict.fromkeys(series, 0)
        ensMin    = series
        ensMax    = series
    else:
        # Combine all series into single one for easy processing
        seriesEnsemble = {} # combine all series into single one
        for seriesId,thisSeries in series.items():
            for t,val in thisSeries.items():
                if not t in seriesEnsemble:
                    seriesEnsemble[t] = []
                seriesEnsemble[t].append(val)

        # Calculate expectation, standard deviation and minimum and maximum values
        ensExp    = {}
        ensStdDev = {}
        ensMin    = {}
        ensMax    = {}
        for t,val in seriesEnsemble.items():
            ensExp[t]    = numpy.average(val)
            ensStdDev[t] = numpy.sqrt(numpy.var(val))
            ensMin[t]    = min(val)
            ensMax[t]    = max(val)

    return ensExp, ensStdDev, ensMin, ensMax

# Plots single series as lines and ensembles of series as their expectation and variance. Optionally plot their range
#  (minimum and maximum values) instead.
def plot(series, minMax = False):
    if isSingleSeries(series):
        # Plot single line
        fig, ax = plotLine(series)
    elif not minMax:
        # Plot expectation and variance
        ensExp, ensStdDev = ensembleStatistics(series)[0:2]
        fig, ax = plotExpectationVariance(ensExp, ensStdDev)
    else:
        # Plot range
        ensMin, ensMax = ensembleStatistics(series)[2:4]
        fig, ax = plotMinMax(ensMin, ensMax)
    return fig, ax

def plotLine(series, fig=None):
    isNewFigure = not fig
    if isNewFigure:
        fig, ax = plt.subplots()
    else:
        ax = fig.get_axes()[0] # TODO correct?

    # Plot single line
    ax.plot(series.keys(), series.values())

    if isNewFigure:
        ax.set(xlabel='time [timestamp]')
        ax.grid()
        # plt.show()
    return fig, ax

def plotExpectationVariance(ensExp, ensStdDev, fig=None):
    isNewFigure = not fig
    if isNewFigure:
        fig, ax = plt.subplots()
    else:
        ax = fig.get_axes()[0] # TODO correct?

    # Plot expectation and variance
    errMinus = ensExp.copy()
    errPlus = ensExp.copy()
    for t in ensExp:
        errMinus[t] -= ensStdDev[t]
        errPlus[t]  += ensStdDev[t]
    plt.plot(ensExp.keys(), ensExp.values())
    plt.fill_between(ensExp.keys(),
                     list(errMinus.values()), list(errPlus.values()),
                     facecolor='blue', alpha=0.15)

    if isNewFigure:
        ax.set(xlabel='time [timestamp]')
        ax.grid()
        # plt.show()
    return fig, ax

def plotMinMax(ensMin, ensMax, fig=None):
    isNewFigure = not fig
    if isNewFigure:
        newFigure = True
        fig, ax = plt.subplots()
    else:
        ax = fig.get_axes()[0] # TODO correct?

    # Plot range (assumes keys are the same for min and max)
    plt.fill_between(ensMin.keys(),
                     list(ensMin.values()), list(ensMax.values()),
                     facecolor='blue', alpha=0.15)

    if isNewFigure:
        ax.set(xlabel='time [timestamp]')
        ax.grid()
        # plt.show()
    return fig, ax

# def drawGraph(series):
#     plt.figure(figsize=(8, 8))
#     nx.draw_networkx(self.graphObj, pos=nx.circular_layout(self.graphObj), node_size=5)
#     # nx.draw_networkx(g, pos=nx.circular_layout(g), node_size=5)
#     # plt.xlim(-0.05, 1.05)
#     # plt.ylim(-0.05, 1.05)
#     plt.axis('off')
#     plt.show()
#
# def drawGraphAgg(self):
#     print("plotting graph")
#     print(list(self.aggGraph.edges()))
#     plt.figure(figsize=(8, 8))
#     nx.draw_networkx(self.aggGraph, pos=nx.circular_layout(self.aggGraph), node_size=5)
#     # plt.xlim(-0.05, 1.05)
#     # plt.ylim(-0.05, 1.05)
#     plt.axis('off')
#     plt.show()

# Sorts a dictionaries values and returns a list of its keys in that sorted order.
# E.g. obtain a list of nodes sorted according to a metric.
def sortKeyByAscVal(series):
    return sorted(list(series.keys()),key=series.get)
def sortKeyByDescVal(series):
    return sorted(list(series.keys()),key=series.get, reverse=True)
