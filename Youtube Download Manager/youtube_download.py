from pytube import YouTube
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import re
import threading

class Application:
    def __init__(self, root):
        self.root=root
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_columnconfigre(0, weight=1)
        self.root.config(bg="ffdddd")

        top_label = Label(self.root, text="Youtube Download Manager", fg='orange',font=('type Xero', 70) )
        top_label.grid(pady=(0,20))

        link_label = Label(self.root, text="Please Paste Any Youtube Video Link Below", font=('SnowPersons',30))
        link_label.grid(pady=(0,20))



if __name__ == "__main__":
    window = Tk()
    window.title("Youtube Download Manager")
    window.state("zoomed")

    app = Application(window)



    mainloop()