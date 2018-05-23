import tkinter as tk


class MeanModelContainer(tk.Frame):
    def __init__(self, parent, frameFactory, meanModels):
        tk.Frame.__init__(self, parent)

        #self.pack(side="left", fill="both", expand=True)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.meanModels = meanModels
        self.frameFactory = frameFactory
        self.currentImage = 0
        #self.image = self.frameFactory.createMeanModelImage(self, meanModel)
        self.frames = self.createFrames()
        self.show()

    def createFrames(self):
        frames = list()
        for i in range(8):
            x, y = self.getXYfromIndex(i)
            frames.append(self.frameFactory.createMeanModelFrame(self, self.meanModels[i][0], x, y))
        return frames
    
    def getXYfromIndex(self, idx):
        if idx < 4:
            y = 0
            x = idx
        else:
            y = 1
            x = idx - 4
        return x, y

    def showNext(self):
        self.show()

    def showPrevious(self):
        self.show()

    def show(self):
        for frame in self.frames:
            frame.tkraise()
