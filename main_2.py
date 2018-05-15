import tkinter as tk
from gui.radiographFrame import RadiographFrame
from src.dataHandler import DataHandler


class MainApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("CV Project")

        self.imgContainer = tk.Frame(self)
        self.imgContainer.pack(side="left", fill="both", expand=True)
        self.imgContainer.grid_rowconfigure(0, weight=1)
        self.imgContainer.grid_columnconfigure(0, weight=1)

        self.buttonContainer = tk.Frame(self)
        self.buttonContainer.pack(side="right", fill="none", expand=True)
        self.buttonContainer.grid_rowconfigure(0, weight=1)
        self.buttonContainer.grid_columnconfigure(0, weight=1)

        self.currentRadiograph = 0

        # Load data
        self.dataHandler = DataHandler()
        self.radioImages = list()
        for radiograph in self.dataHandler.getRadiographs():
            img = radiograph.getImage()
            self.radioImages.append(RadiographFrame(self.imgContainer, img))

        self.showRadiograph()

        self.button = tk.Button(self.buttonContainer, text="Next Radiograph", command=self.showNextRadiograph)
        self.button.grid(row=0, column=1, sticky="nsew", padx=(20,0))

        self.hi_there = tk.Button(self.buttonContainer, text="Previous Radiograph", command=self.showPreviousRadiograph)
        self.hi_there.grid(row=1, column=1, sticky="nsew", pady=(0, 500), padx=(20,0))

    def showNextRadiograph(self):
        if self.currentRadiograph < self.dataHandler.getNBofRadiographs() - 1:
            self.currentRadiograph += 1
        else: 
            self.currentRadiograph = 0

        self.showRadiograph()

    def showPreviousRadiograph(self):
        if self.currentRadiograph > 0:
            self.currentRadiograph -= 1
        else: 
            self.currentRadiograph = self.dataHandler.getNBofRadiographs() - 1

        self.showRadiograph()

    def showRadiograph(self):
        frame = self.radioImages[self.currentRadiograph]
        frame.tkraise()


if __name__ == '__main__':

    app = MainApp()
    app.mainloop()
