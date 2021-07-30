from dataStructures import CloseHashtable

class CrossRoad:
    def __init__(self, TL_id, name, passingCars, TL_mode, TL_currentStatus, reverseCounter):
        self.TL_id = TL_id
        self.name = name
        self.passingCars = passingCars
        self.TL_mode = TL_mode
        self.TL_currentStatus = TL_currentStatus
        self.reverseCounter = reverseCounter

class CrossRoads:
    def __init__(self):
        self.TLlst = CloseHashtable.HashTable()

    def newCrossRoad(self, TL_id, name, passingCars, TL_mode, TL_currentStatus, reverseCounter):
        temp = CrossRoad(TL_id, name, passingCars, TL_mode, TL_currentStatus, reverseCounter)
        self.TLlst.insert(temp.TL_id, temp)
        print(self.TLlst.data)

    def searchCrossRoad(self, TL_id):
        print(self.TLlst.get(TL_id).value.name)
        



test = CrossRoads()
test.newCrossRoad(2, "zand", 4, "custom", "green", 20)
test.searchCrossRoad(2)





# class Agent:
#     def __init__(self, ncode, name, fname):
#         self.ncode = ncode
#         self.name = name
#         self.fname = fname

# class Agents:
#     def __init__(self):
#         self.agnlst = Hashtable.HashTable()

#     def add_agent(self, ncode, name, fname):
#         temp = Agent(ncode, name, fname)
#         self.agnlst[str(ncode)] = temp

#     def search_agent(ncode):
#         return self.agnlst[str(ncode)]

#     def __iter__(self):
#         for key, value in self.agnlst:
#             yield key, value