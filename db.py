from dataStructures import CloseHashtable
import re

"""---------------------------------------
          *   CrossRoad Section  *
---------------------------------------"""
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
     


"""---------------------------------------
          *   Agent Section  *
---------------------------------------"""
class Agent:
    def __init__(self, name, national_code, absentee_time, attendance_time, status, current_TL, shift):
        self.name = name
        self.national_code = national_code
        self.absentee_time = absentee_time
        self.attendance_time = attendance_time
        self.status = status
        self.current_TL = current_TL
        self.shift = shift

class Agents:
    def __init__(self):
        self.agnlst = CloseHashtable.HashTable()
        # self.shifts = CloseHashtable.HashTable()

    def newAgent(self, name, national_code, absentee_time, attendance_time, status, current_TL, next_TL):
        temp = Agent(self, name, national_code, absentee_time, attendance_time, status, current_TL, next_TL)
        self.agnlst.insert(temp.national_code, temp)
        print(self.TLlst.data)
        