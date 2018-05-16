import tkinter as tk
import cv2

from gui.radiographFrame import RadiographFrame
from gui.imageContainer import ImageContainer
from gui.buttonContainer import ButtonContainer
from src.dataHandler import DataHandler
from src.procrustes import Procrustes
from src.frameFactory import FrameFactory


class MainApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("CV Project")

        self.dataHandler = DataHandler()

        self.frameFactory = FrameFactory(self.dataHandler)

        self.imgContainer = ImageContainer(self, self.frameFactory)

        self.buttonContainer = ButtonContainer(self)
        self.buttonContainer.createImageNavigationButtons(self.imgContainer)
        self.buttonContainer.createProcrustedButton(self)

    def performInitialProcrustes(self):
        self.procrustes = Procrustes(self.dataHandler)
        alignedTeeth = self.procrustes.performProcrustesAlignment()


if __name__ == '__main__':

    app = MainApp()
    app.mainloop()
