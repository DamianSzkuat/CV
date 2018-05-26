import tkinter as tk
import numpy as np

from gui.radiographFrame import RadiographFrame

class ModelFittingContainer(tk.Frame):

    def __init__(self, parent, frameFactory, meanModels, radiograph):
        tk.Frame.__init__(self, parent)
        #self.pack(side="left", fill="both", expand=True)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameFactory = frameFactory
        self.meanModels = meanModels
        self.currentRadiograph = 0
        self.radioImage = self.frameFactory.createRadiographFramesFromRadiographs([radiograph], self, self.meanModels, drawLandmarks=False)
        self.show()
        
    def showNext(self):
        self.show()

    def showPrevious(self):
        self.show()

    def show(self):
        frame = self.radioImage[0]
        frame.tkraise()
