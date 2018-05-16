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

        self.imgContainer = ImageContainer(self)

        self.buttonContainer = ButtonContainer(self)

        self.currentRadiograph = 0

        self.dataHandler = DataHandler()

        self.frameFactory = FrameFactory(self.dataHandler)

        self.radioImages = self.createRadiographFrames(drawLandmarks=True)

        self.showRadiograph()

        self.buttonContainer.createBasicButtons(self)

    def performInitialProcrustes(self):
        self.procrustes = Procrustes(self.dataHandler)
        alignedTeeth = self.procrustes.performProcrustesAlignment()

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

    # def drawToothOnImage(self, tooth, img):
    #     for i in range(40):
    #         # Draw Circles
    #         x = int(tooth.getLandmarks()[i][0])
    #         y = int(tooth.getLandmarks()[i][1])
    #         cv2.circle(img, (x, y), 1, (0,255,0), 1)

    #         # Draw line connecting the circles
    #         if i < 39:
    #             x_2 = int(tooth.getLandmarks()[i+1][0])
    #             y_2 = int(tooth.getLandmarks()[i+1][1])
    #         else: 
    #             x_2 = int(tooth.getLandmarks()[0][0])
    #             y_2 = int(tooth.getLandmarks()[0][1])
            
    #         cv2.line(img, (x ,y), (x_2, y_2), (255,0,0))

    #     # Draw center
    #     center = tooth.getCenter()
    #     cv2.circle(img, (int(center[0]), int(center[1])), 5, (0,0,255), 2)
    #     return img

    # def createRadiographFrames(self, drawLandmarks=False):
    #     radioImages = list()
    #     for radiograph in self.dataHandler.getRadiographs():
    #         img = radiograph.getImage()

    #         if drawLandmarks:
    #             img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #             teeth = radiograph.getTeeth()
    #             for tooth in teeth:
    #                img = self.drawToothOnImage(tooth, img)

    #         radioImages.append(RadiographFrame(self.imgContainer, img))

    #     return radioImages


if __name__ == '__main__':

    app = MainApp()
    app.mainloop()
