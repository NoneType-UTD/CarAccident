class Graph:
    def __init__(self):
        self.WindowSize = 0
        self.Table = [[]]
        self.Graph = {}

    def SetWindowSize(self, windowSize: int):
        self.WindowSize = windowSize

    def GetWindowSize(self):
        return self.WindowSize

    def GetGraph(self):
        return self.Graph

    def CreateGraph(self, wordList):
        for i in range(len(wordList)):
            if wordList[i] not in self.Graph:
                self.Graph[wordList[i]] = []
            self.Graph[wordList[i]] += self.FindConnections(wordList, i)

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
