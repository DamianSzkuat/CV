import tkinter as tk


class ModelFittingContainer(tk.Frame):

    def __init__(self, parent, frameFactory):
        tk.Frame.__init__(self, parent)
        #self.pack(side="left", fill="both", expand=True)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameFactory = frameFactory
        self.currentRadiograph = 0
        self.radioImages = self.frameFactory.createRadiographFrames(self, drawLandmarks=False)
        self.show()
        self.bindFrames(parent)

    def key(self, event=None):
        print("pressed", repr(event.char))

    def drawModelOnFrame(self, event=None):
        self.radioImages[self.currentRadiograph] =\
            self.frameFactory.drawTootSethOnFrame(self, self.currentRadiograph, event.x, event.y)
        self.show()

    def bindFrames(self, parent):
        for frame in self.radioImages:
            parent.bind("<Key>", self.key)
            parent.bind("<Button-1>", self.drawModelOnFrame)
            parent.bind("<2>", lambda event: frame.focus_set())

    def showNext(self):
        if self.currentRadiograph < len(self.radioImages) - 1:
            self.currentRadiograph += 1
        else: 
            self.currentRadiograph = 0

        self.show()

    def showPrevious(self):
        if self.currentRadiograph > 0:
            self.currentRadiograph -= 1
        else: 
            self.currentRadiograph = len(self.radioImages) - 1

        self.show()

    def show(self):
        frame = self.radioImages[self.currentRadiograph]
        frame.tkraise()
