import tkinter
from tkinter import ttk
from tkinter import messagebox

class MainWindow(tkinter.Tk):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clock = ClockUi(master = self)
        self.clock.grid(row=0, column=0, padx=5, pady=5)
        self.title("سیستم مدیریت چراغ های راهنمایی")
        self.geometry("800x700")
        self.mainloop()


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
        from app import hour, minute, second, day
        self.clocklbl.config(text=f"{hour} : {minute} : {second}")
        self.daylbl.config(text=f"{day}")
        self.clocklbl.after(100, self.updateClock)


def main():
    Mw = MainWindow()