import tkinter as tk


class ImageContainer(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.pack(side="left", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    
