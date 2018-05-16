import tkinter as tk


class ImageContainer(tk.Frame):

    def __init__(self, parent, frameFactory):
        tk.Frame.__init__(self, parent)

        self.pack(side="left", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameFactory = frameFactory
        self.currentRadiograph = 0
        self.radioImages = self.frameFactory.createRadiographFrames(self, drawLandmarks=True)
        self.showRadiograph()
    
    def showNextRadiograph(self):
        if self.currentRadiograph < len(self.radioImages) - 1:
            self.currentRadiograph += 1
        else: 
            self.currentRadiograph = 0

        self.showRadiograph()

    def showPreviousRadiograph(self):
        if self.currentRadiograph > 0:
            self.currentRadiograph -= 1
        else: 
            self.currentRadiograph = len(self.radioImages) - 1

        self.showRadiograph()

    def showRadiograph(self):
        frame = self.radioImages[self.currentRadiograph]
        frame.tkraise()
