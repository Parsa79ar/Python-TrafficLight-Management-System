from dataStructures import Hashtable

class Agent:
    def __init__(self, ncode, name, fname):
        self.ncode = ncode
        self.name = name
        self.fname = fname

class Agents:
    def __init__(self):
        self.agnlst = Hashtable.HashTable()

    def add_agent(self, ncode, name, fname):
        temp = Agent(ncode, name, fname)
        self.agnlst[str(ncode)] = temp

    def search_agent(ncode):
        return self.agnlst[str(ncode)]

    def __iter__(self):
        for key, value in self.agnlst:
            yield key, value