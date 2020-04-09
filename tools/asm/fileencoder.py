import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.constants import END, LEFT, BOTH


def hex_decode(hex_str):
    print(hex_str)
    b = bytes.fromhex(hex_str.strip())
    return b.decode(encoding='GB18030', errors="ignore")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
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
        text_str = hex_decode(a)
        self.stext.insert('1.0', text_str)



root = tk.Tk()
app = Application(master=root)
app.mainloop()
