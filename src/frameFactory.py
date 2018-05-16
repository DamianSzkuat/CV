import cv2
import numpy as np
from copy import deepcopy

from gui.radiographFrame import RadiographFrame
from gui.singleToothFrame import SingleToorhFrame


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
            # cv2.circle(img, (int(width/2), int(height/2)), 10, (0,255,0), 5)
            tooth.scale(height*5)
            tooth.translate([width/2, height/2])
            print("Tooth: " + str(tooth.getLandmarks()))
            img = self._drawToothOnImage(tooth, img)

            teethImages.append(SingleToorhFrame(parent, img))
        
        return teethImages

    def createRadiographFrames(self, parent, drawLandmarks=False):
        radioImages = list()
        for radiograph in self.dataHandler.getRadiographs():
            img = radiograph.getImage()

            if drawLandmarks:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                teeth = radiograph.getTeeth()
                for tooth in teeth:
                   img = self._drawToothOnImage(tooth, img)

            radioImages.append(RadiographFrame(parent, img))

        return radioImages

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

