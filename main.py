import tkinter as tk
import cv2

from gui.radiographFrameContainer import RadiographFrameContainer
from gui.procrustesTeethTestImageContainer import ProcrustesTeethTestImageContainer
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

        self.radiographFrameContainer = RadiographFrameContainer(self, self.frameFactory)
        self.procrustesTeethTestImageContainer = None

        self.buttonContainer = ButtonContainer(self)
        self.buttonContainer.createImageNavigationButtons(self.radiographFrameContainer)
        self.buttonContainer.createProcrustedButton(self)

    def performInitialProcrustes(self):
        self.procrustes = Procrustes(self.dataHandler)
        alignedTeeth = self.procrustes.performProcrustesAlignment()
        self.procrustesTeethTestImageContainer = ProcrustesTeethTestImageContainer(self, self.frameFactory, alignedTeeth)
        self.buttonContainer.createImageNavigationButtons(self.procrustesTeethTestImageContainer)

if __name__ == '__main__':

    app = MainApp()
    app.mainloop()
