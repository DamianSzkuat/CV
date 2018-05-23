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

    def createMeanModelImage(self, parent, meanModel):
        height = 720
        width = 1280
        img = np.zeros((height,width,3), np.uint8)
        cv2.circle(img, (int(width/2), int(height/2)), 100, (0,0,255), 5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, "Mean Model", (0,height), font, 4,(255,255,255),2,cv2.LINE_AA)
        return MeanModelFrame(parent, img)

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
        meanTooth = Tooth(meanModel)
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

    def createRadiographFrames(self, parent, drawLandmarks=False):
        radioImages = list()
        for radiograph in self.dataHandler.getRadiographs(deepCopy=True):
            img = radiograph.getImage()

            if drawLandmarks:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                teeth = radiograph.getTeeth()
                for tooth in teeth:
                   img = self._drawToothOnImage(tooth, img)

            radioImages.append(RadiographFrame(parent, img))

        return radioImages

    def drawTootSethOnFrame(self, parent, radiograph_index, x_co, y_co):
        # TODO 
        img = self.dataHandler.getRadiographs(deepCopy=True)[radiograph_index].getImage()
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.circle(img, (x_co, y_co), 100, (0,255,0), 5)
        return RadiographFrame(parent, img)

    def _drawTootSethOnImage(self, teethSet, img):
        for i in range(8):
            start = i*40
            end = start + 40
            tooth = Tooth(teethSet.landmarks[start:end])
            img = self._drawToothOnImage(tooth, img)
        
        return img

    def _drawToothOnImage(self, tooth, img):
        for i in range(40):
            # Draw Circles
            x = int(tooth.getLandmarks()[i][0])
            y = int(tooth.getLandmarks()[i][1])
            cv2.circle(img, (x, y), 1, (0,255,0), 1)

            # Draw line connecting the circles
            if i < 39:
                x_2 = int(tooth.getLandmarks()[i+1][0])
                y_2 = int(tooth.getLandmarks()[i+1][1])
            else: 
                x_2 = int(tooth.getLandmarks()[0][0])
                y_2 = int(tooth.getLandmarks()[0][1])
            
            cv2.line(img, (x ,y), (x_2, y_2), (255,0,0))

        # Draw center
        center = tooth.getCenter()
        cv2.circle(img, (int(center[0]), int(center[1])), 5, (0,0,255), 2)
        return img

