import tkinter as tk
import cv2
from copy import deepcopy
import numpy as np

from gui.radiographFrameContainer import RadiographFrameContainer
from gui.procrustesTeethImageContainer import ProcrustesTeethImageContainer
from gui.buttonContainer import ButtonContainer
from gui.meanModelContainer import MeanModelContainer
from gui.manualModelPlacementContainer import ManualModelPlacementContainer
from gui.autoModelPlacementContainer import AutoModelPlacementContainer
from gui.modelFittingContainer import ModelFittingContainer

from src.dataHandler import DataHandler
from src.procrustes import Procrustes
from src.frameFactory import FrameFactory
from src.PCA import PCA
from src.tooth import Tooth
from src.modelFitter import ModelFitter
from src.statisticalModelTrainer import StatisticalModelTrainer
from src.MultiResActiveShapeModel import MultiResolutionActiveShapeModel

from src.filter import Filter


class MainApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("CV Project")

        self.dataHandler = DataHandler(scale_radiographs_by=0.4)
        self.frameFactory = FrameFactory(self.dataHandler)
        self.statisticalModelTrainer = StatisticalModelTrainer()
        self.procrustes = Procrustes()

        self.radiographFrameContainer = RadiographFrameContainer(self, self.frameFactory)
        self.procrustesTeethSetImageContainer = None
        self.modelFittingContainer = None

        self.buttonContainer = ButtonContainer(self)
        self.buttonContainer.createImageNavigationButtons(self.radiographFrameContainer)
        self.buttonContainer.createFunctionButtons(self)

        self.manualModelPlacementContainer = None

        self.alignedTeeth = list()
        self.meanModels = list()
        self.k_pixels = [13,7,2,2,1]
        self.m_pixels = [25,15,4,3,2]
        self.resolutionLevels = 2
        self.filter_settings = [(3, 3, 6), (3, 3, 6), (3, 3, 6), (1, 2, 6), (1, 2, 3)]

        #self.filterTest()
        #self.createMeanModelImages = True        

    def filterTest(self):
        radiograph = self.dataHandler.getRadiographs(deepCopy=True)[0]
        blurred_img = Filter.process_image(deepcopy(radiograph.getImage()), median_kernel=3, bilateral_kernel=10)
        cv2.imshow("BlurredImage", blurred_img)
        clahe = cv2.equalizeHist(blurred_img)
        cv2.imshow("Clahe", clahe)
        img_1 = Filter.laplacian(blurred_img)
        cv2.imshow("Img1", img_1)

        # radiograph.downScale()
        # blurred_img = Filter.process_image(deepcopy(radiograph.getImage()), median_kernel=3, bilateral_kernel=10)
        # img_2 = Filter.laplacian(deepcopy(blurred_img))
        # height = img_1.shape[0]
        # width = img_1.shape[1]
        # img_2 = cv2.resize(img_1, (int(width*0.5), int(height*0.5)))
        # cv2.imshow("Img2", img_2)

        # radiograph.downScale()
        # blurred_img = Filter.process_image(deepcopy(radiograph.getImage()), median_kernel=3, bilateral_kernel=10)
        # img_3 = Filter.laplacian(deepcopy(blurred_img))
        # height = img_2.shape[0]
        # width = img_2.shape[1]
        # img_3 = cv2.resize(img_2, (int(width*0.5), int(height*0.5)))
        # cv2.imshow("Img3", img_3)

        # radiograph.downScale()
        # blurred_img = Filter.process_image(deepcopy(radiograph.getImage()), median_kernel=3, bilateral_kernel=10)
        # img_4 = cv2.Canny(deepcopy(blurred_img), 15, 15)
        # cv2.imshow("Img4", img_4)

        # radiograph.downScale()
        # blurred_img = Filter.process_image(deepcopy(radiograph.getImage()), median_kernel=3, bilateral_kernel=10)
        # img_5 = cv2.Canny(deepcopy(blurred_img), 15, 15)
        # cv2.imshow("Img5", img_5)

    def trainCompleteStatisticalModel(self):
        self.statisticalModel = self.statisticalModelTrainer.trainCompleteStatisticalModel(self.k_pixels, self.resolutionLevels, self.filter_settings, leaveOneOut=0)

        # for i in range(8):
        #     maxEig = self.statisticalModel.getToothModelByIndex(i).getEigenvalues()[0]
        #     print("Tooth " + str(i) + " biggest eigenvalue: " + str(maxEig*10000))

        # if(self.createMeanModelImages):
        #     self.frameFactory.createMeanModelPresentationImages(self.statisticalModel)

    def performManualModelPositionInit(self):
        self.manualModelPlacementContainer = ManualModelPlacementContainer(self, self.frameFactory, self.statisticalModel.getAllToothModels(deepCopy=True))
        self.buttonContainer.createImageNavigationButtons(self.manualModelPlacementContainer)
    
    def acceptModelPosition(self):
        self.manualModelPlacementContainer.nextMeanModel()

    def changeToothRotation(self, var):
        if self.manualModelPlacementContainer is not None:
            self.manualModelPlacementContainer.manualRotation(var)

    def performAutoModelPositionInit(self):
        return None
    
    def performModelFitting(self):
        
        if self.manualModelPlacementContainer is not None:
            initialModelPositions = self.manualModelPlacementContainer.getChosenModelPositions()
            initialModelRotations = self.manualModelPlacementContainer.getChosenModelRotations()
            initialModelPositions *= 2.5

        self.multiResActiveShapeModel = MultiResolutionActiveShapeModel(self.statisticalModel,
                                                                        resolutionLevels=self.resolutionLevels,
                                                                        m_pixels=self.m_pixels,
                                                                        k_pixels=self.k_pixels,
                                                                        filter_settings=self.filter_settings,
                                                                        initialPositions=initialModelPositions,
                                                                        initialRotations=initialModelRotations)
        radiograph = DataHandler().getRadiographs(deepCopy=True)[self.manualModelPlacementContainer.getChosenRadiograph()]

        # Fit the first tooth to the radiograph
        fittedModels_Y = self.multiResActiveShapeModel.fitCompleteModel(radiograph)

        self.fittedModels = list()

        # allign fitted model to be drawn
        for model in fittedModels_Y:
            [X, Y] = model
            temp = self.procrustes.allignModelToData(Y, X)[1]
            self.fittedModels.append(temp)

        self.fittedModels = np.array(self.fittedModels)
        
        print("fittedModels" + str(np.array(self.fittedModels).shape))
        radiograph.scaleImage(0.4)

        self.frameFactory.createFittingErrorPresentationImages(self.fittedModels, radiograph)

        self.modelFittingContainer = ModelFittingContainer(self, self.frameFactory,  [self.fittedModels], radiograph)
        self.buttonContainer.createImageNavigationButtons(self.modelFittingContainer)


if __name__ == '__main__':

    app = MainApp()
    app.mainloop()
