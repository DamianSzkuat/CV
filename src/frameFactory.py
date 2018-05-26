import cv2
import numpy as np
from copy import deepcopy

from gui.radiographFrame import RadiographFrame
from gui.singleToothFrame import SingleToothFrame
from gui.teethSetFrame import TeethSetFrame
from gui.meanModelFrame import MeanModelFrame

from src.tooth import Tooth


class FrameFactory:

    def __init__(self, dataHandler):
        self.dataHandler = dataHandler

    def createProcrustesAlignedTeethImages(self, parent, alignedTeeth):
        teeth = deepcopy(alignedTeeth)
        teethImages = list()
        height = 720
        width = 1280
        for tooth in teeth:
            img = np.zeros((height,width,3), np.uint8)
            tooth.scale(height)
            tooth.translate([width/2, height/2])
            img = self._drawToothOnImage(tooth, img)

            teethImages.append(SingleToothFrame(parent, img))
        
        return teethImages

    def createMeanModelFrame(self, parent, meanModel, col, row):
        height = 360
        width = 320
        img = np.zeros((height,width,3), np.uint8)
        meanTooth = Tooth(deepcopy(meanModel))
        meanTooth.scale(height)
        meanTooth.translate([width/2, height/2])
        img = self._drawToothOnImage(meanTooth, img)
        frame = MeanModelFrame(parent, img, row, col)
        return frame

    def createProcrustesAlignedTeethSetImages(self, parent, alignedTeethSets):
        teethSets = deepcopy(alignedTeethSets)
        teethImages = list()
        height = 720
        width = 1280
        for teethSet in teethSets:
            img = np.zeros((height,width,3), np.uint8)
            teethSet.scale(height*5)
            teethSet.translate([width/2, height/2])
            img = self._drawTootSethOnImage(teethSet, img)

            teethImages.append(TeethSetFrame(parent, img))
        
        return teethImages

    def createLefOutRadiographFrame(self, parent, meanModels=None, drawLandmarks=False):
        radioImages = list()
        i = 0

        radiograph = self.dataHandler.getLeftOutRadiograph(deepCopy=True)
        img = radiograph.getImage()

        if drawLandmarks:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            teeth = radiograph.getTeeth()
            for tooth in teeth:
                img = self._drawToothOnImage(tooth, img)

        if meanModels is not None:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            for model in meanModels[i]:
                img = self._drawToothOnImage(model, img)

        radioImages.append(RadiographFrame(parent, img))

        return radioImages

    def createRadiographFrames(self, parent, meanModels=None, drawLandmarks=False):
        radioImages = list()
        i = 0
        for radiograph in self.dataHandler.getRadiographs(deepCopy=True):
            img = radiograph.getImage()

            if drawLandmarks:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                teeth = radiograph.getTeeth()
                for tooth in teeth:
                   img = self._drawToothOnImage(tooth, img)

            if meanModels is not None:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                for model in meanModels[i]:
                    img = self._drawToothOnImage(model, img)

            radioImages.append(RadiographFrame(parent, img))
            i += 1

        return radioImages

    def createRadiographFramesFromRadiographs(self, radiographs, parent, meanModels=None, drawLandmarks=False):
        radioImages = list()
        i = 0
        for radiograph in radiographs:
            img = radiograph.getImage()

            if drawLandmarks:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                teeth = radiograph.getTeeth()
                for tooth in teeth:
                   img = self._drawToothOnImage(tooth, img)

            if meanModels is not None:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                for model in meanModels[i]:
                    img = self._drawToothOnImage(model, img)

            radioImages.append(RadiographFrame(parent, img))
            i += 1

        return radioImages

    def drawToothModelOnFrame(self, parent, radiograph_index, meanModels, model_index, modelLocations):
        img = self.dataHandler.getRadiographs(deepCopy=True)[radiograph_index].getImage()
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        for i in range(model_index+1):
            model = deepcopy(meanModels[i])
            model = Tooth(model)
            model.scale(200)
            model.translate(modelLocations[i])
            img = self._drawToothOnImage(model, img)

        return RadiographFrame(parent, img), 

    def _drawTootSethOnImage(self, teethSet, img):
        for i in range(8):
            start = i*40
            end = start + 40
            tooth = Tooth(teethSet.landmarks[start:end])
            img = self._drawToothOnImage(tooth, img)
        
        return img

    def _drawToothOnImage(self, tooth, img, landmarkColor=(0,255,0), lineColor=(255,0,0), centerColor=(0,0,255)):
        for i in range(40):
            # Draw Circles
            x = int(tooth.getLandmarks()[i][0])
            y = int(tooth.getLandmarks()[i][1])
            cv2.circle(img, (x, y), 1, landmarkColor, 1)

            # Draw line connecting the circles
            if i < 39:
                x_2 = int(tooth.getLandmarks()[i+1][0])
                y_2 = int(tooth.getLandmarks()[i+1][1])
            else: 
                x_2 = int(tooth.getLandmarks()[0][0])
                y_2 = int(tooth.getLandmarks()[0][1])
            
            cv2.line(img, (x ,y), (x_2, y_2), lineColor)

        # Draw center
        center = tooth.getCenter()
        cv2.circle(img, (int(center[0]), int(center[1])), 5, centerColor, 2)
        return img

