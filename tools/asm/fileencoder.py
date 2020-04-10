import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.constants import END, LEFT, BOTH
from tkinter import ttk


def hex_decode(hex_str, encoding):
    print(hex_str)
    b = bytes.fromhex(hex_str.strip())

    return b.decode(encoding=encoding, errors="ignore")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.combbox = ttk.Combobox(self, values=["utf-8", 'gbk', 'GB18030', 'utf-16'])
        self.combbox.set('GB18030')
        self.combbox.pack(side="top")

        self.text = ScrolledText(self)
        self.text.pack(side="top")

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "转换"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.stext = ScrolledText(bg='white', height=10)
        self.stext.pack(fill=BOTH, side=LEFT, expand=True)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        a = self.text.get('0.0', 'end')

        text_str = hex_decode(a, self.combbox.get())

        self.stext.insert('1.0', text_str)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
