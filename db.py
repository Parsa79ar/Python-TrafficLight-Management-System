from dataStructures import CloseHashtable
import re

class CrossRoad:
    def __init__(self, TL_id, name, NS_passingCars, EW_passingCars, TL_mode, NS_light, EW_light, NS_timer, EW_timer, NS_time, EW_time, NS, EW):
        self.TL_id = TL_id
        self.name = name
        self.NS_passingCars = NS_passingCars
        self.EW_passingCars = EW_passingCars
        self.TL_mode = TL_mode
        self.NS_light = NS_light
        self.EW_light = EW_light
        self.NS_timer = NS_timer
        self.EW_timer = EW_timer
        self.NS_time = NS_time
        self.EW_time = EW_time
        self.NS = NS
        self.EW = EW

class CrossRoads:
    def __init__(self):
        self.TLlst = CloseHashtable.HashTable()

    def newCrossRoad(self, TL_id, name):
        # 1 = green auto - 0 = custom red
        temp = CrossRoad(TL_id, name, 5, 10, 1, 1, 0, 10, 10, 10, 10, 1, 0)
        self.TLlst.insert(temp.TL_id, temp)
        print(self.TLlst.data)

    def searchCrossRoad(self, x):
        lst = []
        for elm in self.TLlst.travers():
            txt = f"{elm.value.TL_id} {elm.value.name}"
            test = re.search(x, txt)
            if test:
                lst.append(elm)
        return lst

    # def searchCrossRoad(self, TL_id):
    #     return self.TLlst.get(TL_id)

    def traversCrossRoads(self):
        yield from self.TLlst.travers() 
     





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