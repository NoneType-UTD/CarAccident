class Graph(object):
    def __init__(self, windowSize):
        self.WindowSize = windowSize
        self.Table = [[]]
        self.Graph = {}

    def GetWindowSize(self):
        return self.WindowSize

    def GetGraph(self):
        return self.Graph

    def GetValues(self, key):
        return self.Graph[key]

    def CreateGraph(self, wordList):
        for i in range(len(wordList)):
            if wordList[i] not in self.Graph:
                self.Graph[wordList[i]] = []
            connections = self.FindConnections(wordList, i)
            for _ in connections:
                if _ not in self.Graph[wordList[i]]:
                    self.Graph[wordList[i]].append(_)
            # self.Graph[wordList[i]] += self.FindConnections(wordList, i)

    def FindConnections(self, wordList, index):
        connections = []
        indexConnections = []
        for x in (number + 1 for number in range(self.WindowSize)):
            if index - x >= 0:
                indexConnections = [index - x] + indexConnections
            if index + x < len(wordList):
                indexConnections.append(index + x)
        for x in indexConnections:
            connections.append(wordList[x])
        return connections

    def MergeGraphs(self, newGraph):
        for k in newGraph.GetGraph().keys():
            newValues = newGraph.GetValues(k)
            if k not in self.Graph.keys():
                self.Graph[k] = []
            for v in newValues:
                if v not in self.Graph[k]:
                    self.Graph[k].append(v)
