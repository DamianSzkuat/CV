import tkinter as tk
import cv2

from gui.radiographFrameContainer import RadiographFrameContainer
from gui.procrustesTeethImageContainer import ProcrustesTeethImageContainer
from gui.buttonContainer import ButtonContainer
from gui.meanModelContainer import MeanModelContainer
from gui.modelFittingContainer import ModelFittingContainer
from src.dataHandler import DataHandler
from src.procrustes import Procrustes
from src.frameFactory import FrameFactory
from src.PCA import PCA


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
        self.buttonContainer.createTeethSwapButtons(self)

        self.alignedTeeth = list()
        self.meanModels = list()

    def performInitialProcrustes(self):
        self.procrustes = Procrustes()
        
        self.alignedTeeth = list()
        for i in range(8):
            temp = self.dataHandler.getAllTeethAtIndex(i, deepCopy=True)
            self.alignedTeeth.append(self.procrustes.performProcrustesAlignment(temp))
        self.showProcrustesTeethAtIndex(0)
    
    def showProcrustesTeethAtIndex(self, idx):
        self.procrustesTeethImageContainer = ProcrustesTeethImageContainer(self, self.frameFactory, self.alignedTeeth[idx])
        self.buttonContainer.createImageNavigationButtons(self.procrustesTeethImageContainer)

    def perfromPCA(self):
        self.pca = PCA()

        self.meanModels = list()
        for i in range(8):
            self.meanModels.append(self.pca.do_pca_and_build_model(self.alignedTeeth[i]))

        

        self.meanModelContainer = MeanModelContainer(self, self.frameFactory, self.meanModels)
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
