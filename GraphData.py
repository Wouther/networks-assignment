import csv


class GraphData:
    fileName = ""

    def __init__(self, fileName):
        print("constructing new GraphData instance from file", fileName)
        self.loadFile(fileName)

    def loadFile(self, fileName):
        # TODO check if file exists and is valid csv file
        self.fileName = fileName
        with open(fileName, 'r') as dataFile:
            dbCSV = csv.reader(dataFile, delimiter='\t', quotechar='"')
            for row in dbCSV:
                print(",", row)

        return True  # TODO don't always return true
