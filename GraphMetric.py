# Helper functions to manipulate data series from a TemporalGraph.
#
# One series is formatted as a dictionary keyed by timestamps. Multiple series are a dictionary of series keyed by some
# identifying value for the series (e.g. seed node) and the series itself as value.

import numpy

def isSingleSeries(series):
    return not type(list(series.values())[0]) is dict

# Calculate statistics across the different data series (ensemble), i.e. expected value and standard deviation.
def ensembleStatistics(series):
    ensExp    = {} # ensemble expectation
    ensStdDev = {} # ensemble standard deviation

    if isSingleSeries(series):
        ensExp    = series
        ensStdDev = dict.fromkeys(series, 0)
    else:
        # Combine all series into single one for easy processing
        seriesEnsemble = {} # combine all series into single one
        for seriesId,thisSeries in series.items():
            for t,val in thisSeries.items():
                if not t in seriesEnsemble:
                    seriesEnsemble[t] = []
                seriesEnsemble[t].append(val)

        # Calculate expectation and standard deviation
        for t,val in seriesEnsemble.items():
            ensExp[t]    = numpy.average(val)
            ensStdDev[t] = numpy.sqrt(numpy.var(val))

    return ensExp, ensStdDev
