from time import sleep
import tkinter
from tkinter import ttk
from tkinter import messagebox
import db

day = hour = minute = second = 0
tmpLight = tmpSMS = None
crossRoad_id = 0
crossRoads = db.CrossRoads()

def init(light, sms):
    global tmpLight, tmpSMS
    tmpLight = light
    tmpSMS = sms

def clock():
    global day, hour, minute, second
    second += 1
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour += 1
    if hour == 24:
        hour = 0
        day += 1
    setLight()

def attendance(crossRoad_id, nationalCode):
    pass


def setLight():
    global crossRoads
    for cr in crossRoads.traversCrossRoads():
        if cr.value.NS_light == 1:
            if cr.value.NS_timer == 0:
                # TL_id - NS = 0 or EW = 1 - red chnage to 1 and green change to 0
                passingCars = tmpLight(cr.key, 0, 1)
                if cr.value.TL_mode == 1:
                    if passingCars >= (2 * cr.value.NS_time):
                        cr.value.NS_time = 2 * cr.value.NS_time
                cr.value.NS_timer = cr.value.NS_time
                tmpLight(cr.key, 1, 0)
                cr.value.NS_light = 0
                cr.value.EW_light = 1
            else:    
                cr.value.NS_timer -= 1

        elif cr.value.EW_light == 1:
            if cr.value.EW_timer == 0:
                # TL_id - NS = 0 or EW = 1 - red chnage to 1 and green change to 0
                passingCars = tmpLight(cr.key, 0, 1)
                if cr.value.TL_mode == 1:
                    if passingCars >= (2 * cr.value.EW_time):
                        cr.value.EW_time = 2 * cr.value.EW_time
                cr.value.EW_timer = cr.value.EW_time
                tmpLight(cr.key, 1, 0)
                cr.value.EW_light = 0
                cr.value.NS_light = 1
            else:    
                cr.value.EW_timer -= 1




"""---------------------------------------
          *   Ui Section  *
---------------------------------------"""
class MainWindow(tkinter.Tk):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clock = ClockUi(master = self)
        self.clock.grid(row=0, column=0, padx=125, pady=20)
        tkinter.Button(self, text="مدیریت چهارراه ها", padx=20, pady=20, command=self.crossRoadWindow).grid(row=1, column=0, pady=10)
        tkinter.Button(self, text="مدیریت مامور ها", padx=23, pady=20, command=self.crossRoadWindow).grid(row=2, column=0, pady=10)
        self.title("سیستم مدیریت چراغ های راهنمایی")
        self.geometry("350x300")
        self.mainloop()

    def crossRoadWindow(self):
        CrossRoadUi(self)

class CrossRoadUi(tkinter.Toplevel):
    def __init__(self, master, **kwargs):
        super(CrossRoadUi, self).__init__(master, **kwargs)

        # Clock 
        self.clock = ClockUi(master = self)
        self.clock.pack(padx=5, pady=5)

        # Label Frames
        self.wrapper1 = tkinter.LabelFrame(self, text="لیست چهارراه ها")
        self.wrapper2 = tkinter.LabelFrame(self, text="جست وجو")
        self.wrapper3 = tkinter.LabelFrame(self, text="اطلاعات چهارراه")
        self.wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

        # CrossRoad TreeView
        self.trv = ttk.Treeview(self.wrapper1, columns=(1,2,3,4,5,6,7,8,9), show="headings", height="10")
        self.trv.pack()
        self.trv.column(1, width=60, anchor="center")
        self.trv.column(2, width=150, anchor="center")
        self.trv.column(3, width=150, anchor="center")
        self.trv.column(4, width=150, anchor="center")
        self.trv.column(5, width=150, anchor="center")
        self.trv.column(6, width=150, anchor="center")
        self.trv.column(7, width=150, anchor="center")
        self.trv.column(8, width=150, anchor="center")
        self.trv.column(9, width=150, anchor="center")
        self.trv.heading(1, text="چهارراه ID")
        self.trv.heading(2, text="نام")
        self.trv.heading(3, text="ماشین های شمال-جنوب")
        self.trv.heading(4, text="ماشین های شرق-غرب")
        self.trv.heading(5, text="حالت چهارراه")
        self.trv.heading(6, text="چراغ شمال-جنوب")
        self.trv.heading(7, text="چراغ شرق-غرب")
        self.trv.heading(8, text="زمان شمال-جنوب")
        self.trv.heading(9, text="زمان شرق-غرب")
        self.trv.bind('<Double 1>', self.getrow)

        # Search Section
        self.searchTrv = ttk.Treeview(self.wrapper2, columns=(1,2,3,4,5,6,7,8,9), show="headings", height="2")
        self.searchTrv.pack()
        self.searchTrv.column(1, width=60, anchor="center")
        self.searchTrv.column(2, width=150, anchor="center")
        self.searchTrv.column(3, width=150, anchor="center")
        self.searchTrv.column(4, width=150, anchor="center")
        self.searchTrv.column(5, width=150, anchor="center")
        self.searchTrv.column(6, width=150, anchor="center")
        self.searchTrv.column(7, width=150, anchor="center")
        self.searchTrv.column(8, width=150, anchor="center")
        self.searchTrv.column(9, width=150, anchor="center")
        self.searchTrv.heading(1, text="چهارراه ID")
        self.searchTrv.heading(2, text="نام")
        self.searchTrv.heading(3, text="ماشین های شمال-جنوب")
        self.searchTrv.heading(4, text="ماشین های شرق-غرب")
        self.searchTrv.heading(5, text="حالت چهارراه")
        self.searchTrv.heading(6, text="چراغ شمال-جنوب")
        self.searchTrv.heading(7, text="چراغ شرق-غرب")
        self.searchTrv.heading(8, text="زمان شمال-جنوب")
        self.searchTrv.heading(9, text="زمان شرق-غرب")
        self.searchTrv.bind('<Double 1>', self.getrow)

        self.lbl = tkinter.Label(self.wrapper2, text="جست و جو")
        self.lbl.pack(side=tkinter.LEFT, padx=10)
        self.ent = tkinter.Entry(self.wrapper2)
        self.ent.pack(side=tkinter.LEFT, padx=6)
        self.btn = tkinter.Button(self.wrapper2, text="جست و جو", command=self.search)
        self.btn.pack(side=tkinter.LEFT, padx=6)
        self.cbtn = tkinter.Button(self.wrapper2, text="Refresh", command=self.clear)
        self.cbtn.pack(side=tkinter.LEFT, padx=6)

        # User Data Section
        self.lbl1 = tkinter.Label(self.wrapper3, text="چهارراه ID", state="disabled")
        self.lbl1.grid(row=0, column=0, padx=5, pady=3)
        self.ent1 = tkinter.Entry(self.wrapper3, state="disabled")
        self.ent1.grid(row=0, column=1, padx=5, pady=3)

        self.lbl2 = tkinter.Label(self.wrapper3, text="نام")
        self.lbl2.grid(row=1, column=0, padx=5, pady=3)
        self.ent2 = tkinter.Entry(self.wrapper3)
        self.ent2.grid(row=1, column=1, padx=5, pady=3)

        self.up_btn = tkinter.Button(self.wrapper3, text="Update", command=self.update_crossRoad)
        self.add_btn = tkinter.Button(self.wrapper3, text="Add New", command=self.add_crossRoad)
        self.delete_btn = tkinter.Button(self.wrapper3, text="Delete", command=self.delete_crossRoad)
        self.up_btn.grid(row=4, column=0, padx=5, pady=3)
        self.add_btn.grid(row=4, column=1, padx=5, pady=3)
        self.delete_btn.grid(row=4, column=2, padx=5, pady=3)

        self.geometry("1330x800")
        self.title("مدیریت چهارراه ها")
        self.update()


    """---------------------------------------
            *   Ui Methods Section  *
    ---------------------------------------"""  
    def add_crossRoad(self):
        global crossRoad_id
        crossRoad_name = self.ent2.get()
        crossRoads.newCrossRoad(crossRoad_id, crossRoad_name)
        tmpLight(crossRoad_id, 0, 0)
        crossRoad_id += 1


    def update(self):
        self.trv.delete(*self.trv.get_children())
        for i  in crossRoads.traversCrossRoads():
            self.trv.insert('', 'end', values=(i.value.TL_id, i.value.name, i.value.NS_passingCars, i.value.EW_passingCars, i.value.TL_mode, i.value.NS_light, i.value.EW_light, i.value.NS_timer, i.value.EW_timer))
        self.trv.after(400, self.update)
    

    def search(self):
        q2 = self.ent.get()
        
        
    def clear(self):
        update()

    def getrow(self, event):
        rowid = self.trv.identify_row(event.y)
        item = self.trv.item(trv.focus()) 
        self.ent1.insert(0, item['values'][0])   
        self.ent2.insert(0, item['values'][0])   
        self.ent3.insert(0, item['values'][0])   
        self.ent4.insert(0, item['values'][0])   
      

    def update_crossRoad(self):
        crossRoad_name = self.ent2.get()
        crossRoad_passingCars = self.ent3.get()
        crossRoad_TL_mode = self.ent4.get()
        if messagebox.askyesno("Confirm Update?", "Are you sure you want to change this crossRoad?"):
            pass


    def delete_crossRoad(self):
        crossRoad_id = self.ent1.get()
        if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this crossRoad?"):
            pass

"""---------------------------------------
          *  Clock Ui Section  *
---------------------------------------"""
class ClockUi(tkinter.Frame):
    def __init__(self, master):
        super(ClockUi, self).__init__(master, bd=3, relief="ridge")
        self.timelbl = tkinter.Label(self, text="ساعت:")
        self.timelbl.grid(row=0, column=0, padx=5)
        self.clocklbl = tkinter.Label(self)
        self.clocklbl.grid(row=0, column=1)
        self.dayslbl = tkinter.Label(self, text="روز : ")
        self.dayslbl.grid(row=1, column=0, padx=2)
        self.daylbl = tkinter.Label(self)
        self.daylbl.grid(row=1, column=1)
        self.updateClock()

    def updateClock(self):
        self.clocklbl.config(text=f"{hour} : {minute} : {second}")
        self.daylbl.config(text=f"{day}")
        self.clocklbl.after(250, self.updateClock)


"""---------------------------------------
          *   Run Ui  *
---------------------------------------"""
def main():
    Mw = MainWindow()