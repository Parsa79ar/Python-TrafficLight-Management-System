import tkinter
from tkinter import ttk
from tkinter import messagebox
import db

day = hour = minute = second = 0
tmpLight = tmpSMS = NS_light_color = EW_light_color  =  None
crossRoad_id = 0
crossRoads = db.CrossRoads()
agents = db.Agents()

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
    checkShift()

def attendance(TL_id, national_code):
    print(TL_id)
    print(national_code)


def setLight():
    global crossRoads
    for cr in crossRoads.traversCrossRoads():
        if cr.value.NS == 1:
            if cr.value.NS_timer <= 0:
                if cr.value.NS_timer == 0:
                    # TL_id - NS = 0 or EW = 1 - red chnage to 1 and green change to 0
                    passingCars = tmpLight(cr.key, 0, 1)
                    if cr.value.TL_mode == 1:
                        if passingCars >= (2 * cr.value.NS_time):
                            cr.value.NS_time = 2 * cr.value.NS_time
                    cr.value.NS_light = 0
                if cr.value.NS_timer == -3:
                    cr.value.NS = 0
                    cr.value.EW = 1
                    cr.value.EW_light = 1
                    cr.value.NS_timer = cr.value.NS_time
                    tmpLight(cr.key, 1, 0)
                    continue    
            cr.value.NS_timer -= 1

        elif cr.value.EW == 1:
            if cr.value.EW_timer <= 0:
                if cr.value.EW_timer == 0:
                    # TL_id - NS = 0 or EW = 1 - red chnage to 1 and green change to 0
                    passingCars = tmpLight(cr.key, 1, 1)
                    if cr.value.TL_mode == 1:
                        if passingCars >= (2 * cr.value.EW_time):
                            cr.value.EW_time = 2 * cr.value.EW_time
                    cr.value.EW_light = 0
                if cr.value.EW_timer == -3:
                    cr.value.NS = 1
                    cr.value.EW = 0
                    cr.value.NS_light = 1
                    cr.value.EW_timer = cr.value.EW_time
                    tmpLight(cr.key, 0, 0)
                    continue    
            cr.value.EW_timer -= 1


def checkShift():
    for i  in agents.traversAgents():
        if i.value.shift.storage[0]:
            if (i.value.shift.storage[0].key - 600) == ((hour * 3600) + (minute * 60) + second):
                agent_nc = i.value.national_code
                cr_id = i.value.shift.storage[0].value[0]
                tmpSMS(agent_nc, cr_id)


"""---------------------------------------
          *   Ui Section  *
---------------------------------------"""
class MainWindow(tkinter.Tk):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clock = ClockUi(master = self)
        self.clock.grid(row=0, column=0, padx=125, pady=20)
        tkinter.Button(self, text="مدیریت چهارراه ها", padx=20, pady=20, command=self.crossRoadWindow).grid(row=1, column=0, pady=10)
        tkinter.Button(self, text="مدیریت مامور ها", padx=23, pady=20, command=self.agentWindow).grid(row=2, column=0, pady=10)
        self.title("سیستم مدیریت چراغ های راهنمایی")
        self.geometry("350x300")
        self.mainloop()

    def crossRoadWindow(self):
        CrossRoadUi(self)

    def agentWindow(self):
        AgentUi(self)


"""---------- CrossRoad Ui -----------"""
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

        # User Data Section
        self.lbl1 = tkinter.Label(self.wrapper3, text="چهارراه ID", state="disabled")
        self.lbl1.grid(row=0, column=0, padx=5, pady=3)
        self.lbl1_value = tkinter.Label(self.wrapper3, text=crossRoad_id, state="disabled")
        self.lbl1_value.grid(row=0, column=1, padx=2, pady=3)
    
        self.lbl2 = tkinter.Label(self.wrapper3, text="نام")
        self.lbl2.grid(row=1, column=0, padx=5, pady=3)
        self.ent2 = tkinter.Entry(self.wrapper3)
        self.ent2.grid(row=1, column=1, padx=5, pady=3)

        self.lbl3 = tkinter.Label(self.wrapper3, text="زمان شمال-جنوب", state="disabled")
        self.lbl3.grid(row=2, column=0, padx=5, pady=3)
        self.ent3 = tkinter.Entry(self.wrapper3, state="disabled")
        self.ent3.grid(row=2, column=1, padx=5, pady=3)

        self.lbl4 = tkinter.Label(self.wrapper3, text="زمان شرق-غرب", state="disabled")
        self.lbl4.grid(row=3, column=0, padx=5, pady=3)
        self.ent4 = tkinter.Entry(self.wrapper3, state="disabled")
        self.ent4.grid(row=3, column=1, padx=5, pady=3)

        self.add_btn = tkinter.Button(self.wrapper3, text="ثبت چهارراه", command=self.add_crossRoad, padx=10, pady=5)
        self.up_btn = tkinter.Button(self.wrapper3, text="آپدیت چهارراه", command=self.update_crossRoad, padx=5, pady=5, state="disabled")
        self.auto_mode_btn = tkinter.Button(self.wrapper3, text="حالت اتوماتیک", command=self.auto_mode, padx=5, pady=5, state="disabled")
        self.custom_mode_btn = tkinter.Button(self.wrapper3, text="حالت دستی", command=self.custom_mode, padx=12, pady=5, state="disabled")
        self.add_btn.grid(row=1, column=3, padx=10, pady=5)
        self.up_btn.grid(row=2, column=3, padx=10, pady=5)
        self.auto_mode_btn.grid(row=1, column=4, padx=20, pady=5)
        self.custom_mode_btn.grid(row=2, column=4, padx=20, pady=5)

        self.geometry("1330x800")
        self.title("مدیریت چهارراه ها")
        self.update()


    """---------- CrossRoads Methods Ui -----------"""
    def add_crossRoad(self):
        global crossRoad_id
        crossRoad_name = self.ent2.get()
        crossRoads.newCrossRoad(crossRoad_id, crossRoad_name)
        tmpLight(crossRoad_id, 0, 0)
        crossRoad_id += 1
        self.lbl1_value.config(text=crossRoad_id)
        self.ent2.delete(0, "end")


    def update(self):
        self.trv.delete(*self.trv.get_children())
        for i  in crossRoads.traversCrossRoads():
            if i.value.NS_light == 1:
                NS_light_color = "سبز"
            elif i.value.NS_light == 0:
                NS_light_color = "قرمز"

            if i.value.EW_light == 1:
                EW_light_color = "سبز"
            elif i.value.EW_light == 0:
                EW_light_color = "قرمز"
            
            if i.value.NS == 1:
                NS_timer = i.value.NS_timer
                EW_timer = i.value.NS_timer + 3
                if NS_timer < 0:
                    NS_timer = 0
            elif i.value.EW == 1:
                EW_timer = i.value.EW_timer
                NS_timer = i.value.EW_timer + 3
                if EW_timer < 0:
                    EW_timer = 0

            self.trv.insert('', 'end', values=(i.value.TL_id, i.value.name, i.value.NS_passingCars, i.value.EW_passingCars, i.value.TL_mode, NS_light_color, EW_light_color, NS_timer, EW_timer))
        self.trv.after(400, self.update)
    

    def search(self):
        if self.ent.get():
            self.searchTrv.delete(*self.searchTrv.get_children())
            searchValue = self.ent.get()
            for i in crossRoads.searchCrossRoad(searchValue):
                if i:
                    if i.value.NS_light == 1:
                        NS_light_color = "سبز"
                    elif i.value.NS_light == 0:
                        NS_light_color = "قرمز"

                    if i.value.EW_light == 1:
                        EW_light_color = "سبز"
                    elif i.value.EW_light == 0:
                        EW_light_color = "قرمز"

                    self.searchTrv.insert('', 'end', values=(i.value.TL_id, i.value.name, i.value.NS_passingCars, i.value.EW_passingCars, i.value.TL_mode, NS_light_color, EW_light_color, i.value.NS_timer, i.value.EW_timer))
                self.searchTrv.after(400, self.search)
        else:
            self.searchTrv.delete(*self.searchTrv.get_children())


    def auto_mode(self):
        select = crossRoads.TLlst.get(int(self.item[0]))
        if select.value.TL_mode != 1:
            select.value.TL_mode = 1


    def custom_mode(self):
        self.custom_flag = 1
        self.lbl3.config(state="normal")
        self.lbl4.config(state="normal")
        self.ent3.config(state="normal")
        self.ent4.config(state="normal")
        self.up_btn.config(state="normal")


    def getrow(self, event):
        rowid = self.trv.identify_row(event.y)
        self.item = self.trv.item(self.trv.focus(), 'values')
        if self.item:
            self.add_btn.config(state="disabled")
            self.lbl1_value.config(text=self.item[0])
            self.ent2.delete(0, "end")   
            self.ent2.insert(0, self.item[1])
            self.auto_mode_btn.config(state="normal")      
            self.custom_mode_btn.config(state="normal")      


    def update_crossRoad(self):
        select = crossRoads.TLlst.get(int(self.item[0]))
        crossRoad_name = self.ent2.get()
        if self.custom_flag == 1:
            NS_time = self.ent3.get()
            EW_time = self.ent4.get()
        
        if messagebox.askyesno("اعمال تغییرات؟", "آیا از تغییر چهارراه مطمئن هستید؟"):
            select.value.name = crossRoad_name
            if self.custom_flag == 1:
                if select.value.TL_mode != 0:
                    select.value.TL_mode = 0
                select.value.NS_time = int(NS_time)
                select.value.EW_time = int(EW_time)
                self.ent2.delete(0, "end")
                self.ent3.delete(0, "end")
                self.ent4.delete(0, "end")
                self.ent3.config(state="disabled")
                self.ent4.config(state="disabled")
                self.lbl3.config(state="disabled")
                self.lbl4.config(state="disabled")
                self.add_btn.config(state="normal")
                self.up_btn.config(state="disabled")
                self.lbl1_value.config(text=crossRoad_id)
                self.custom_mode_btn.config(state="disabled")
                self.auto_mode_btn.config(state="disabled")


"""------------ Agent Ui -------------"""
class AgentUi(tkinter.Toplevel):
    def __init__(self, master, **kwargs):
        super(AgentUi, self).__init__(master, **kwargs)

        # Clock 
        self.clock = ClockUi(master = self)
        self.clock.pack(padx=5, pady=5)

        # Label Frames
        self.wrapper1 = tkinter.LabelFrame(self, text="لیست مامور ها")
        self.wrapper2 = tkinter.LabelFrame(self, text="جست وجو")
        self.wrapper3 = tkinter.LabelFrame(self, text="اطلاعات مامور")
        self.wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

        # Agent TreeView
        self.trv = ttk.Treeview(self.wrapper1, columns=(1,2,3,4,5,6), show="headings", height="10")
        self.trv.pack()
        self.trv.column(1, width=150, anchor="center")
        self.trv.column(2, width=150, anchor="center")
        self.trv.column(3, width=150, anchor="center")
        self.trv.column(4, width=150, anchor="center")
        self.trv.column(5, width=150, anchor="center")
        self.trv.column(6, width=150, anchor="center")
        self.trv.heading(1, text="نام")
        self.trv.heading(2, text="کدملی")
        self.trv.heading(3, text="زمان غیبت")
        self.trv.heading(4, text="زمان حضوری")
        self.trv.heading(5, text="وضعیت کنونی")
        self.trv.heading(6, text="چهارراه فعلی")
        self.trv.bind('<Double 1>', self.getrow)

        # Search Section
        self.searchTrv = ttk.Treeview(self.wrapper2, columns=(1,2,3,4,5,6), show="headings", height="2")
        self.searchTrv.pack()
        self.searchTrv.column(1, width=150, anchor="center")
        self.searchTrv.column(2, width=150, anchor="center")
        self.searchTrv.column(3, width=150, anchor="center")
        self.searchTrv.column(4, width=150, anchor="center")
        self.searchTrv.column(5, width=150, anchor="center")
        self.searchTrv.column(6, width=150, anchor="center")
        self.searchTrv.heading(1, text="نام")
        self.searchTrv.heading(2, text="کدملی")
        self.searchTrv.heading(3, text="زمان غیبت")
        self.searchTrv.heading(4, text="زمان حضوری")
        self.searchTrv.heading(5, text="وضعیت کنونی")
        self.searchTrv.heading(6, text="چهارراه فعلی")
        self.searchTrv.bind('<Double 1>', self.getrow)

        self.lbl = tkinter.Label(self.wrapper2, text="جست و جو")
        self.lbl.pack(side=tkinter.LEFT, padx=10)
        self.ent = tkinter.Entry(self.wrapper2)
        self.ent.pack(side=tkinter.LEFT, padx=6)
        self.btn = tkinter.Button(self.wrapper2, text="جست و جو", command=self.search)
        self.btn.pack(side=tkinter.LEFT, padx=6)

        # User Data Section
        self.lbl1 = tkinter.Label(self.wrapper3, text="نام مامور")
        self.lbl1.grid(row=0, column=0, padx=5, pady=3)
        self.ent1 = tkinter.Entry(self.wrapper3)
        self.ent1.grid(row=0, column=1, padx=5, pady=3)
    
        self.lbl2 = tkinter.Label(self.wrapper3, text="کدملی")
        self.lbl2.grid(row=1, column=0, padx=5, pady=3)
        self.ent2 = tkinter.Entry(self.wrapper3)
        self.ent2.grid(row=1, column=1, padx=5, pady=3)

        self.add_btn = tkinter.Button(self.wrapper3, text="ثبت مامور", command=self.add_agent, padx=10, pady=5)
        self.up_btn = tkinter.Button(self.wrapper3, text="آپدیت مامور", command=self.update_agent, padx=5, pady=5, state="disabled")
        self.add_btn.grid(row=0, column=3, padx=10, pady=5)
        self.up_btn.grid(row=1, column=3, padx=10, pady=5)


        """------------ Shifts Ui -------------"""
        # Label Frames
        self.frm = tkinter.Frame(self)
        self.frm.pack(fill="both", expand="yes")
        self.wrapper4 = tkinter.LabelFrame(self.frm, text="لیست شیفت ها")
        self.wrapper5 = tkinter.LabelFrame(self.frm, text="اطلاعات شیفت")
        self.wrapper4.grid(row=0, column=0, padx=20, pady=10)
        self.wrapper5.grid(row=0, column=1, padx=20, pady=10)

        # Shifts TreeView
        self.Shifttrv = ttk.Treeview(self.wrapper4, columns=(1,2,3), show="headings", height="5")
        self.Shifttrv.grid(padx=30, pady=23)
        self.Shifttrv.column(1, width=150, anchor="center")
        self.Shifttrv.column(2, width=150, anchor="center")
        self.Shifttrv.column(3, width=150, anchor="center")
        self.Shifttrv.heading(1, text="چهارراه ID")
        self.Shifttrv.heading(2, text="کد ملی مامور")
        self.Shifttrv.heading(3, text="زمان شیفت")
        self.Shifttrv.bind('<Double 1>', self.getrow)

        # Shift Data Section
        self.slbl1 = tkinter.Label(self.wrapper5, text="چهارراه ID")
        self.slbl1.grid(row=0, column=0, padx=10, pady=12)
        self.sent1 = tkinter.Entry(self.wrapper5)
        self.sent1.grid(row=0, column=1, padx=10, pady=12)

        self.slbl2 = tkinter.Label(self.wrapper5, text="کد ملی مامور")
        self.slbl2.grid(row=1, column=0, padx=10, pady=12)
        self.sent2 = tkinter.Entry(self.wrapper5)
        self.sent2.grid(row=1, column=1, padx=10, pady=12)
    
        self.slbl3 = tkinter.Label(self.wrapper5, text="زمان شیفت : ")
        self.slbl3.grid(row=2, column=0, padx=10)
        self.slbl4 = tkinter.Label(self.wrapper5, text="ساعت - دقیقه")
        self.slbl4.grid(row=2, column=1, padx=10)
        self.slbl5 = tkinter.Label(self.wrapper5, text="ساعت")
        self.slbl5.grid(row=3, column=0, padx=10, pady=5)
        self.sent3 = tkinter.Entry(self.wrapper5)
        self.sent3.grid(row=3, column=1, padx=10, pady=5)
        self.slbl6 = tkinter.Label(self.wrapper5, text="دقیقه")
        self.slbl6.grid(row=4, column=0, padx=10, pady=5)
        self.sent4 = tkinter.Entry(self.wrapper5)
        self.sent4.grid(row=4, column=1, padx=10, pady=5)

        self.s_add_btn = tkinter.Button(self.wrapper5, text="ثبت شیفت", command=self.add_shift, padx=10, pady=5)
        self.s_up_btn = tkinter.Button(self.wrapper5, text="آپدیت شیفت", command=self.update_shift, padx=5, pady=5, state="disabled")
        self.s_add_btn.grid(row=0, column=3, padx=25, pady=5)
        self.s_up_btn.grid(row=1, column=3, padx=25, pady=5)

        self.geometry("970x920")
        self.title("مدیریت مامورها")
        self.update()


    """---------- Agent Methods Ui -----------"""
    def add_agent(self):
        agent_name = self.ent1.get()
        agent_ncode = int(self.ent2.get())
        agents.newAgent(agent_name, agent_ncode)
        self.ent1.delete(0, "end")
        self.ent2.delete(0, "end")


    def update(self):
        self.trv.delete(*self.trv.get_children())
        for i  in agents.traversAgents():
            self.trv.insert('', 'end', values=(i.value.name, i.value.national_code, i.value.absentee_time, i.value.attendance_time, i.value.status, i.value.current_TL))
        self.trv.after(400, self.update)
    

    def search(self):
        if self.ent.get():
            self.searchTrv.delete(*self.searchTrv.get_children())
            searchValue = self.ent.get()
            for i in agents.searchAgent(searchValue):
                if i:
                    self.searchTrv.insert('', 'end', values=(i.value.name, i.value.national_code, i.value.absentee_time, i.value.attendance_time, i.value.status, i.value.current_TL))
                self.searchTrv.after(400, self.search)
        else:
            self.searchTrv.delete(*self.searchTrv.get_children())


    def getrow(self, event):
        rowid = self.trv.identify_row(event.y)
        self.item = self.trv.item(self.trv.focus(), 'values')
        if self.item:
            self.up_btn.config(state="normal")
            self.add_btn.config(state="disabled")
            self.ent1.delete(0, "end")   
            self.ent1.insert(0, self.item[0])
            self.ent2.delete(0, "end")   
            self.ent2.insert(0, self.item[1])     


    def update_agent(self):
        select = agents.agnlst.get(int(self.item[1]))
        agent_name = self.ent1.get()
        national_code = self.ent2.get()

        select.value.name = agent_name
        select.value.national_code = int(national_code)
        
        if messagebox.askyesno("اعمال تغییرات؟", "آیا از تغییر مامور مطمئن هستید؟"):
                self.ent1.delete(0, "end")
                self.ent2.delete(0, "end")
                self.add_btn.config(state="normal")
                self.up_btn.config(state="disabled")


    """---------- Shifts Methods Ui -----------"""
    def add_shift(self):
        tl_id = int(self.sent1.get())
        agent_nc = int(self.sent2.get())
        shift_time_h = int(self.sent3.get())
        shift_time_m = int(self.sent4.get())
        
        get_agent = agents.getAgent(agent_nc)
        if get_agent:
            shift_time = (shift_time_h * 3600) + (shift_time_m * 60)
            start_shift = None
            values = [tl_id, start_shift]
            get_agent.value.shift.insert(shift_time, values)

        self.s_update()
        self.sent1.delete(0, "end")
        self.sent2.delete(0, "end")
        self.sent3.delete(0, "end")


    def s_update(self):
        self.Shifttrv.delete(*self.Shifttrv.get_children())
        for i  in agents.traversAgents():
            self.Shifttrv.insert('', 'end', values=(i.value.shift.storage[0].value[0], i.value.national_code, i.value.shift.storage[0].key))
        self.Shifttrv.after(400, self.update)


    def update_shift():
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