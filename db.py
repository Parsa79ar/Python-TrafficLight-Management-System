from dataStructures import CloseHashtable
from dataStructures import MinHeap
import re

"""---------------------------------------
          *   CrossRoad Section  *
---------------------------------------"""
class CrossRoad:
    def __init__(self, TL_id, name):
        self.TL_id = TL_id
        self.name = name
        self.NS_passingCars = 5
        self.EW_passingCars = 10
        self.TL_mode = 1
        self.NS_light = 1
        self.EW_light = 0
        self.NS_timer = 10
        self.EW_timer = 10
        self.NS_time = 10
        self.EW_time = 10
        self.NS = 1
        self.EW = 0
        self.NC_agent = 0

class CrossRoads:
    def __init__(self):
        self.TLlst = CloseHashtable.HashTable()

    def newCrossRoad(self, TL_id, name):
        # 1 = green auto - 0 = custom red
        temp = CrossRoad(TL_id, name)
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

    def getCrossRoad(self, TL_id):
        return self.TLlst.get(TL_id)

    def traversCrossRoads(self):
        yield from self.TLlst.travers() 
     


"""---------------------------------------
          *   Agent Section  *
---------------------------------------"""
class Agent:
    def __init__(self, name, national_code):
        self.name = name
        self.national_code = national_code
        self.absentee_time = None
        self.attendance_time = None
        self.status = 0    # present => 1 , absentee => 0
        self.current_TL = None
        self.shift = MinHeap.MinHeap()

class Agents:
    def __init__(self):
        self.agnlst = CloseHashtable.HashTable()

    def newAgent(self, name, national_code):
        temp = Agent(name, national_code)
        self.agnlst.insert(temp.national_code, temp)
        print(self.agnlst.data)

    def searchAgent(self, x):
        lst = []
        for elm in self.agnlst.travers():
            txt = f"{elm.value.name} {elm.value.national_code}"
            test = re.search(x, txt)
            if test:
                lst.append(elm)
        return lst

    def getAgent(self, national_code):
        return self.agnlst.get(national_code)
    
    def traversAgents(self):
        yield from self.agnlst.travers()