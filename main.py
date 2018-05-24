import tkinter as tk
import cv2
from copy import deepcopy

from gui.radiographFrameContainer import RadiographFrameContainer
from gui.procrustesTeethImageContainer import ProcrustesTeethImageContainer
from gui.buttonContainer import ButtonContainer
from gui.meanModelContainer import MeanModelContainer
from gui.manualModelPlacementContainer import ManualModelPlacementContainer
from gui.autoModelPlacementContainer import AutoModelPlacementContainer
from src.dataHandler import DataHandler
from src.procrustes import Procrustes
from src.frameFactory import FrameFactory
from src.PCA import PCA
from src.tooth import Tooth
from src.modelFitter import ModelFitter


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
        self.manualModelPlacementContainer = ManualModelPlacementContainer(self, self.frameFactory, self.meanModels)
        self.buttonContainer.createImageNavigationButtons(self.manualModelPlacementContainer)
    
    def acceptModelPosition(self):
        self.manualModelPlacementContainer.nextMeanModel()

    def performAutoModelPositionInit(self):
        self.procrustes = Procrustes()
        radiographs = self.dataHandler.getRadiographs(deepCopy=True)
        self.initializedMeanModels = list()

        for radiograph in radiographs:
            teeth = radiograph.getTeeth(deepCopy=True)
            modelset = list()
            for i in range(8):
                tooth = teeth[i]
                model = deepcopy(self.meanModels[i][0])
                model = Tooth(model)
                temp = self.procrustes.allignModelToData(tooth, model)[1]
                modelset.append(temp)
            self.initializedMeanModels.append(modelset)

        self.autoModelPlacementContainer = AutoModelPlacementContainer(self, self.frameFactory, self.initializedMeanModels)
        self.buttonContainer.createImageNavigationButtons(self.autoModelPlacementContainer)
    
    def performModelFitting(self):
        self.modelFitter = ModelFitter()
        radiographs = self.dataHandler.getRadiographs(deepCopy=True)

        self.fittedModels = list()
        for radiograph in radiographs:
            teeth = radiograph.getTeeth(deepCopy=True)
            modelset = list()
            for i in range(8):
                tooth = deepcopy(teeth[i])
                model = deepcopy(self.meanModels[i][0])
                model = Tooth(model)
                full_model = [model, deepcopy(self.meanModels[i][1]), deepcopy(self.meanModels[i][2])]

                # Fit the model to the radiograph
                fitted_model = self.modelFitter.fitModel(deepcopy(tooth), full_model)

                # allign fitted model to be drawn
                temp = self.procrustes.allignModelToData(deepcopy(tooth), fitted_model)[1]
                modelset.append(temp)

            self.fittedModels.append(modelset)
        
        self.autoModelPlacementContainer = AutoModelPlacementContainer(self, self.frameFactory,  self.fittedModels)
        self.buttonContainer.createImageNavigationButtons(self.autoModelPlacementContainer)

        


        
if __name__ == '__main__':

    app = MainApp()
    app.mainloop()
