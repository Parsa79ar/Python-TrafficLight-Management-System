# by Esmail :)
from ui import main
import tkinter
import app
from typing import Dict, Union, Callable, TypeVar, Generic, List
from random import randint
from threading import Thread
from time import sleep, localtime, time_ns
T = TypeVar("T")


class Console:
    def __init__(self):
        self.data: List[str] = []
        self.callback = None

    def write(self, data: str):
        if self.callback:
            self.callback(data)
        self.data.append(data)

    def read_all(self):
        for i in self.data:
            yield i

    def set_callback(self, callback: Callable[[str], None]):
        self.callback = callback


class Queue(Generic[T]):
    def __init__(self):
        self.arr: List[T] = []

    def dequeue(self) -> T:
        if self.arr:
            return self.arr.pop()

    def enqueue(self, data: T):
        self.arr.insert(0, data)

    def front(self) -> T:
        if self.arr:
            return self.arr[-1]


class Intersection:
    def __init__(self, intersection_id: str):
        self.id = intersection_id
        self.north_south: bool = False  # Green
        self.east_west: bool = False  # Red
        self.traffic_north = 0  # car count in north side
        self.traffic_east = 0
        self.traffic_left_north = 0  # total cars left from current period
        self.traffic_left_east = 0
        # these two variables are defined to insert cars into each side
        #   slightly, if each clock 0.2 car must get into side, 0.2 will be
        #   added to current value, whenever it reached 1, one car will be
        #   injected. writer: I think my brain is going to explode. :)
        self.traffic_east_waiting_to_inject = 0
        self.traffic_north_waiting_to_inject = 0
        self.agent: Union[None, str] = None  # No one is here
        self.traffic_passed = 0

    def add_traffic_north(self, amount: int):
        self.traffic_left_north += amount

    def add_traffic_east(self, amount: int):
        self.traffic_left_east += amount

    def clock(self, time_left: int):
        if time_left == 0:
            x = self.traffic_left_north
        else:
            self.traffic_north_waiting_to_inject += \
                self.traffic_left_north / time_left
            x = int(self.traffic_north_waiting_to_inject)
            self.traffic_north_waiting_to_inject -= x
        self.traffic_left_north -= x
        self.traffic_north += x
        if time_left == 0:
            x = self.traffic_left_east
        else:
            self.traffic_east_waiting_to_inject += \
                self.traffic_left_east / time_left
            x = int(self.traffic_east_waiting_to_inject)
            self.traffic_east_waiting_to_inject -= x
        self.traffic_left_east -= x
        self.traffic_east += x
        if self.north_south and self.traffic_north >= 2:
            self.traffic_north -= 2
            self.traffic_passed += 2
        elif self.east_west and self.traffic_east >= 2:
            self.traffic_east -= 2
            self.traffic_passed += 2

    def change_light(self, side: int, color: int, console: Console):
        amount = 0
        if side == 0 and color == 0 and self.east_west:
            console.write(f"Both sides are Green at {self.id}.")
        elif side == 1 and color == 0 and self.north_south:
            console.write(f"Both sides are Green at {self.id}.")
        elif side == 0:
            if color == 1 and self.north_south:  # changing to red
                amount = self.traffic_passed
                self.traffic_passed = 0
            self.north_south = not color
            console.write(f"{self.id}: North-South changed to "
                          f"{'Red' if color else 'Green'}.")
        elif side == 1:
            if color == 1 and self.east_west:  # changing to red
                amount = self.traffic_passed
                self.traffic_passed = 0
            self.east_west = not color
            console.write(f"{self.id}: East-West changed to "
                          f"{'Red' if color else 'Green'}.")
        return amount

    def set_agent(self, agent_id: str):
        self.agent = agent_id


class AgentNode:
    def __init__(self, agent_id: str, intersection_id: str, _time: int):
        self.id = agent_id
        self.intersection = intersection_id
        self.time = _time + 600


class Simulator:
    def __init__(self,
                 console: Console,
                 clock_callback: Callable,
                 attendance_callback: Callable,
                 clock_speed_callback: Callable
                 ):
        self.clock_callback = clock_callback
        self.attendance_callback = attendance_callback
        self.console = console
        self.intersections: Dict[str, Intersection] = {}
        self.sleep_timer = 990  # millisecond
        self.agents_queue: Queue[AgentNode] = Queue()
        self.time = 0
        self.clock_speed_callback = clock_speed_callback
        self.n_e_callback = None

    def set_new_intersection_callback(self, callback: Callable):
        self.n_e_callback = callback

    def light(self, intersection_id: str, side: int, color: int):
        assert 0 <= side < 2
        assert 0 <= color < 2
        if intersection_id not in self.intersections:
            self.intersections[intersection_id] = intersection =\
                Intersection(intersection_id)
            if self.n_e_callback:
                self.n_e_callback(intersection)
            first = randint(0, int(1.5*(599-(self.time % 600))))
            second = randint(0, int(0.5*first))
            intersection.add_traffic_north(second)
            intersection.add_traffic_east(first - second)
        return self.intersections[intersection_id].change_light(side, color,
                                                                self.console)

    def sms(self, agent_id: str, intersection_id: str):
        ag = AgentNode(agent_id, intersection_id, self.time)
        self.console.write(f"Agent {agent_id} got SMS for {intersection_id}")
        self.agents_queue.enqueue(ag)

    def clock_setter(self, delay: int):
        self.sleep_timer = delay

    def mainloop(self):
        #  Here is the event loop
        while True:
            while True:
                ag = self.agents_queue.front()
                if ag and ag.time == self.time:
                    self.agents_queue.dequeue()
                    self.attendance_callback(ag.intersection, ag.id)
                    self.intersections[ag.intersection].agent = ag.id
                    self.console.write(f"Agent {ag.id} attended"
                                       f" at {ag.intersection}.")
                else:
                    break
            # Traffic Process:
            if self.time == 0 or self.time % 600 == 0:  # new period has began
                for intersection in self.intersections.values():
                    first = randint(100, 800)
                    second = randint(50, first-50)
                    intersection.add_traffic_north(second)
                    intersection.add_traffic_east(first-second)
            if self.time != 0:
                time_left = 599 - (self.time % 600)
                for intersection in self.intersections.values():
                    intersection.clock(time_left)
            self.time += 1
            self.clock_callback()
            self.clock_speed_callback()
            if self.sleep_timer:
                sleep(self.sleep_timer/1000)


class ClockSpeed:
    def __init__(self):
        self.current = 0
        self.size = 5
        self.data = [0.0] * self.size

    def clock(self):
        self.data[self.current] = time_ns()
        self.current = (self.current + 1) % self.size

    def get_avg(self) -> float:
        ls = []
        for i in range(self.current, self.current+self.size-1):
            ls.append(self.data[(i+1) % self.size] - self.data[i % self.size])
        if sum(ls) != 0:
            return round(1/(sum(ls) / ((self.size-1)*10**9)), 2)
        else:
            return 0.0


class Panel(tkinter.Tk):
    class ClockSpeedView(tkinter.Frame):
        def __init__(self, master, clock_speed_callback: Callable[[], float],
                     speed_setter_callback: Callable[[int], None]):
            super(Panel.ClockSpeedView, self).__init__(master, bd=1,
                                                       relief="solid")
            self.clock_speed_callback = clock_speed_callback
            self.speed_setter_callback = speed_setter_callback
            frame = tkinter.Frame(self)
            frame.grid(row=1, column=1)
            tkinter.Label(frame, text="Clock Speed:").grid(row=1, column=1,
                                                           padx=5)
            self.lab_speed = tkinter.Label(frame, text="N/A")
            self.lab_speed.grid(row=1, column=2, padx=5)
            self.scale = tkinter.Scale(self, from_=0, to=1999,
                                       orient="horizontal", showvalue=0,
                                       command=self.scale_callback)
            self.scale.grid(row=2, column=1, pady=5)
            self.scale.set(2000-990)
            self.scale_label = tkinter.Label(self, text="990ms")
            self.scale_label.grid(row=3, column=1)

        def scale_callback(self, _):
            data = 2000 - self.scale.get()
            if data == 1:
                self.scale_label.config(text="Max")
            else:
                self.scale_label.config(text=f"{data}ms")
            self.speed_setter_callback(data)

        def clock(self):
            speed = self.clock_speed_callback()
            if speed == 0:
                out = "N/A"
            elif speed < 999:
                out = f"{speed}Hz"
            elif speed < 999999:
                out = f"{round(speed/1000, 2)}KHz"
            else:
                out = f"{round(speed/1000000, 2)}MHz"
            self.lab_speed.config(text=out)

    class ConsoleView(tkinter.Frame):
        def __init__(self, master):
            super(Panel.ConsoleView, self).__init__(master, bd=1,
                                                    relief="solid")
            tkinter.Label(self, text="Console").grid(row=1, column=1,
                                                     sticky="w")
            self.text = tkinter.Text(self, width=40)
            self.text.grid(row=2, column=1, sticky="nsew")

        def add(self, data: str):
            self.text.insert("end", f"{data}\n")

    class IntersectionView(tkinter.Frame):
        def __init__(self, master, intersection: Intersection):
            super(Panel.IntersectionView, self).__init__(master, bd=1,
                                                         relief="solid")
            self.intersection = intersection
            tkinter.Label(self, text=intersection.id).grid(row=1, column=1)
            self.canvas = tkinter.Canvas(self, width=100, height=100)
            self.canvas.grid(row=2, column=1, pady=5)
            self.canvas.create_line(5, 50, 100, 50)
            self.canvas.create_line(50, 5, 50, 100)
            self.c_north = self.canvas.create_oval(45, 5, 55, 15, fill="red")
            self.c_south = self.canvas.create_oval(45, 90, 55, 100, fill="red")
            self.c_east = self.canvas.create_oval(5, 45, 15, 55, fill="red")
            self.c_west = self.canvas.create_oval(90, 45, 100, 55, fill="red")
            self.c_t_north = self.canvas.create_text(65, 10, text="0")
            self.c_t_east = self.canvas.create_text(10, 65, text="0")
            self.lab_agent = tkinter.Label(self, text="Agent")
            self.lab_agent.grid(row=3, column=1)

        def clock(self):
            if self.intersection.north_south:
                self.canvas.itemconfig(self.c_north, fill="green")
                self.canvas.itemconfig(self.c_south, fill="green")
            else:
                self.canvas.itemconfig(self.c_north, fill="red")
                self.canvas.itemconfig(self.c_south, fill="red")
            if self.intersection.east_west:
                self.canvas.itemconfig(self.c_east, fill="green")
                self.canvas.itemconfig(self.c_west, fill="green")
            else:
                self.canvas.itemconfig(self.c_east, fill="red")
                self.canvas.itemconfig(self.c_west, fill="red")
            self.canvas.itemconfig(self.c_t_east,
                                   text=self.intersection.traffic_east)
            self.canvas.itemconfig(self.c_t_north,
                                   text=self.intersection.traffic_north)
            self.lab_agent.config(text=f"Agent{self.intersection.agent}")

    class IntersectionsView(tkinter.Frame):
        def __init__(self, master,
                     intersections: List[Intersection]):
            super(Panel.IntersectionsView, self).__init__(master, bd=1,
                                                          relief="solid")
            self.intersections = intersections
            self.clocks = []
            self.page = 0
            self.rows = rows = 2
            self.cols = cols = 2
            self.inters: List[List[Union[None, Panel.IntersectionView]]] = \
                [[None]*cols for _ in range(rows)]
            self.but_next = tkinter.Button(self, text="Next",
                                           command=self.next)
            self.but_next.grid(row=rows, column=cols-1, sticky="e",
                               padx=2, pady=2)
            self.but_prev = tkinter.Button(self, text="Prev",
                                           state="disabled",
                                           command=self.prev)
            self.but_prev.grid(row=rows, column=0, sticky="w",
                               padx=2, pady=2)
            self.but_size = tkinter.Button(self, text=f"{rows}x{cols}",
                                           command=self.resize,
                                           relief="solid")
            self.but_size.grid(row=rows+1, column=0, padx=2, pady=2)
            self.load()

        def resize(self):
            cols = Panel.GetIntegerPanel(self, "Enter Width").get_data()
            if cols:
                rows = Panel.GetIntegerPanel(self,
                                             "Enter Height").get_data()
                if rows:
                    self.but_size.config(text=f"{rows}x{cols}")
                    self.rows = rows
                    self.cols = cols
                    self.page = 0
                    for i in self.inters:
                        for j in i:
                            j: Panel.IntersectionView
                            if j:
                                j.grid_forget()
                    self.inters = [[None]*cols for _ in range(rows)]
                    self.load()
                else:
                    print("Wrong Dimensions")

        def next(self):
            self.page += 1
            self.load()

        def prev(self):
            self.page -= 1
            self.load()

        def load(self):
            current = self.page * self.cols * self.rows
            if self.page == 0:
                self.but_prev.config(state="disabled")
            else:
                self.but_prev.config(state="normal")
            if (self.page+1) * self.rows * self.cols >= \
                    len(self.intersections):
                self.but_next.config(state="disabled")
            else:
                self.but_next.config(state="normal")
            for i in self.inters:
                for j in i:
                    if j:
                        j.grid_forget()
            self.clocks.clear()
            for i in range(self.rows):
                for j in range(self.cols):
                    if current >= len(self.intersections):
                        return
                    inter = self.intersections[current]
                    inter = Panel.IntersectionView(self, inter)
                    inter.grid(row=i, column=j, padx=5, pady=5,
                               ipadx=5, ipady=5)
                    self.clocks.append(inter.clock)
                    self.inters[i][j] = inter
                    current += 1

        def new_intersection(self, intersection: Intersection):
            self.intersections.append(intersection)
            if (self.page+1) * self.rows * self.cols < len(self.intersections):
                self.but_next.config(state="normal")
            self.load()

        def clock(self):
            for i in self.clocks:
                i()

    class GetIntegerPanel(tkinter.Toplevel):
        def __init__(self, master, message: str):
            super(Panel.GetIntegerPanel, self).__init__(master)
            self.transient(master)
            tkinter.Label(self, text=message).grid(row=1, column=1,
                                                   padx=5, pady=5)
            self.ent = tkinter.Entry(self)
            self.ent.grid(row=2, column=1, padx=5, pady=5)
            tkinter.Button(self, text="OK",
                           command=self.submit).grid(row=3, column=1,
                                                     padx=5, pady=5)
            self.err = tkinter.Label(self, fg="red")
            self.data = None

        def submit(self):
            if self.ent.get().isnumeric():
                self.data = int(self.ent.get())
                self.destroy()
            else:
                self.err.grid(row=4, column=1, padx=5, pady=5)
                self.err.config(text="Enter Integer Please")

        def get_data(self) -> Union[None, int]:
            if self.data is None:
                self.wait_window()
            return self.data

    class DetailView(tkinter.Frame):
        def __init__(self, master,
                     clock_getter_callback: Callable[[], int]):
            super(Panel.DetailView, self).__init__(master, bd=1,
                                                   relief="solid")
            self.clock_number = tkinter.Label(self, text="Clock:")
            self.clock_number.grid(row=1, column=1)
            self.time_left = tkinter.Label(self, text="Next Period:")
            self.time_left.grid(row=2, column=1)
            self.time = tkinter.Label(self, text="Time:")
            self.time.grid(row=3, column=1)
            self.clock_getter = clock_getter_callback

        def clock(self):
            n = self.clock_getter()
            self.clock_number.config(text=f"Clock: {n}")
            self.time_left.config(text=f"Next Period:{599-(n%600)}")
            b = localtime(73800+n)
            self.time.config(text=f"Time:{b.tm_hour}:{b.tm_min}:{b.tm_sec}")

    def __init__(self, clock_speed_callback: Callable,
                 speed_setter_callback: Callable,
                 clock_number_getter: Callable,
                 intersections: List[Intersection],
                 ):
        super(Panel, self).__init__()
        self.title("Simulator")
        self.c_s_v = Panel.ClockSpeedView(self, clock_speed_callback,
                                          speed_setter_callback)
        self.c_s_v.grid(row=1, column=1, padx=5, pady=5)
        self.d_v = Panel.DetailView(self, clock_number_getter)
        self.d_v.grid(row=1, column=2, padx=5, pady=5)
        self.c_v = Panel.ConsoleView(self)
        self.c_v.grid(row=2, column=1, pady=5, padx=5)
        self.i_v = Panel.IntersectionsView(self, intersections)
        self.i_v.grid(row=2, column=2, padx=5, pady=5)
        self.event_loop()

    def event_loop(self):
        self.c_s_v.clock()
        self.i_v.clock()
        self.d_v.clock()
        self.after(250, self.event_loop)

    def add_to_console(self, data: str):
        self.c_v.add(data)

    def add_intersection(self, intersection: Intersection):
        self.i_v.new_intersection(intersection)


if __name__ == '__main__':
    sim: Union[None, Simulator] = None
    clock_speed = ClockSpeed()
    _console = Console()

    def thread_runner():
        global sim
        sim = Simulator(console=_console,
                        clock_callback=app.clock,
                        attendance_callback=app.attendance,
                        clock_speed_callback=clock_speed.clock)
        sim.mainloop()

    def thread_gui():
        if sim:
            panel = Panel(clock_speed_callback=clock_speed.get_avg,
                          speed_setter_callback=sim.clock_setter,
                          intersections=list(sim.intersections.values()),
                          clock_number_getter=lambda: sim.time)
            panel.attributes('-topmost', True)
            sim.set_new_intersection_callback(panel.add_intersection)
            _console.set_callback(panel.add_to_console)
            app.init(sim.light, sim.sms)
            panel.mainloop()
        else:
            raise TypeError(f"Simulator didn't defined within "
                            f"0.5sec of waiting for "
                            f"thread to create it")
    thread = Thread(name="Core", target=thread_runner)
    thread2 = Thread(name="GUI", target=thread_gui)
    thread3 = Thread(name="MAIN", target=main)
    thread.start()
    thread.join(0.5)
    thread2.start()
    thread3.start()
