import tkinter as tk
import cv2

from gui.radiographFrameContainer import RadiographFrameContainer
from gui.procrustesTeethSetImageContainer import ProcrustesTeethSetImageContainer
from gui.buttonContainer import ButtonContainer
from gui.meanModelContainer import MeanModelContainer
from gui.modelFittingContainer import ModelFittingContainer
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
        self.procrustesTeethSetImageContainer = None
        self.modelFittingContainer = None

        self.buttonContainer = ButtonContainer(self)
        self.buttonContainer.createImageNavigationButtons(self.radiographFrameContainer)
        self.buttonContainer.createFunctionButtons(self)

    def performInitialProcrustes(self):
        self.procrustes = Procrustes()
        teethSets = self.dataHandler.getAllTeethSets()
        alignedTeethSets = self.procrustes.performProcrustesAlignment(teethSets)
        self.procrustesTeethSetImageContainer = ProcrustesTeethSetImageContainer(self, self.frameFactory, alignedTeethSets)
        self.buttonContainer.createImageNavigationButtons(self.procrustesTeethSetImageContainer)
    
    def perfromPCA(self):
        #TODO PCA 
        self.meanModelContainer = MeanModelContainer(self, self.frameFactory, None)
        self.buttonContainer.createImageNavigationButtons(self.meanModelContainer)

    def performManualModelPositionInit(self):
        #TODO Model Fitting
        self.modelFittingContainer = ModelFittingContainer(self, self.frameFactory)
        self.buttonContainer.createImageNavigationButtons(self.modelFittingContainer)
    
    def performAutoModelPositionInit(self):
        #TODO
        return None
    
    def performModelFitting(self):
        #TODO
        return None

        
if __name__ == '__main__':

    app = MainApp()
    app.mainloop()
