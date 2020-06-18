import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.constants import END, LEFT, BOTH
from tkinter import ttk
from autoblood import Mir2GameHelper


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.helper = None

    def create_widgets(self):
        self.combbox = ttk.Combobox(self, values=["昆仑长留战区 - 一刀九九九", '昆仑长留战区 - 无中生有'])
        self.combbox.set('昆仑长留战区 - 无中生有')
        self.combbox.pack(side="top")

        self.L1 = tk.Label(self, text="血量下限")
        self.L1.pack(side=LEFT)
        self.input = tk.Entry(self, bd=5)
        self.input.insert(0, '1000')
        self.input.pack(side=tk.LEFT)

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "启动"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="right")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.do_close)
        self.quit.pack(side="right")

        self.stext = ScrolledText(bg='white', height=10)
        self.stext.pack(fill=BOTH, side=LEFT, expand=True)

    def say_hi(self):
        limit_blood = self.input.get()
        print(limit_blood)
        win_title = self.combbox.get()
        self.helper = Mir2GameHelper(win_title=win_title, limit_blood=int(limit_blood))
        self.stext.insert('1.0', limit_blood + '\n')
        self.stext.insert('1.0', win_title + '\n')
        self.helper.auto_add_blood()

    def do_close(self):
        self.helper.close_helper()
        self.master.destroy()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
