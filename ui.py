import tkinter
from tkinter import ttk
from tkinter import messagebox

class MainWindow(tkinter.Tk):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clock = ClockUi(master = self)
        self.clock.pack()
        self.title("Traffic lights management system")
        self.geometry("800x700")
        self.mainloop()


class ClockUi(tkinter.Frame):
    def __init__(self, master):
        super(ClockUi, self).__init__(master)
        self.timelbl = tkinter.Label(self, text="Time:")
        self.timelbl.grid(row=0, column=0)
        self.clocklbl = tkinter.Label(self)
        self.clocklbl.grid(row=0, column=1)
        self.dayslbl = tkinter.Label(self, text=" - day : ")
        self.dayslbl.grid(row=0, column=2)
        self.daylbl = tkinter.Label(self)
        self.daylbl.grid(row=0, column=3)
        self.updateClock()

    def updateClock(self):
        from app import hour, minute, second, day
        self.clocklbl.config(text=f"{hour} : {minute} : {second}")
        self.daylbl.config(text=f"{day}")
        self.clocklbl.after(100, self.updateClock)


def main():
    Mw = MainWindow()