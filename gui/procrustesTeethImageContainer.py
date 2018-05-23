import tkinter as tk


class ProcrustesTeethImageContainer(tk.Frame):

    def __init__(self, parent, frameFactory, alignedTeeth):
        tk.Frame.__init__(self, parent)

        #self.pack(side="left", fill="both", expand=True)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameFactory = frameFactory
        self.currentTeethSet = 0
        self.teethImages = self.frameFactory.createProcrustesAlignedTeethImages(self, alignedTeeth)
        self.show()
    
    def showNext(self):
        if self.currentTeethSet < len(self.teethImages) - 1:
            self.currentTeethSet += 1
        else: 
            self.currentTeethSet = 0

        self.show()

    def showPrevious(self):
        if self.currentTeethSet > 0:
            self.currentTeethSet -= 1
        else: 
            self.currentTeethSet = len(self.teethImages) - 1

        self.show()

    def show(self):
        frame = self.teethImages[self.currentTeethSet]
        frame.tkraise()
