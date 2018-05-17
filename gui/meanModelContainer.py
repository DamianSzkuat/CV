import tkinter as tk


class MeanModelContainer(tk.Frame):
    def __init__(self, parent, frameFactory, meanModel):
        tk.Frame.__init__(self, parent)

        #self.pack(side="left", fill="both", expand=True)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameFactory = frameFactory
        self.currentImage = 0
        self.image = self.frameFactory.createMeanModelImage(self, meanModel)
        self.show()
    
    def showNext(self):
        self.show()

    def showPrevious(self):
        self.show()

    def show(self):
        frame = self.image
        frame.tkraise()