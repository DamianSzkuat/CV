import numpy as np
import cv2

from src.tooth import Tooth


class Radiograph:
    imgPath = None
    teeth = None
    radiographID = None

    def __init__(self):
        self.teeth = list()
        self.nb_teeth = 8
        self.image = None

    def loadRadiograph(self, radiographID, hasLandmarks=False):
        self.radiographID = radiographID
        self.imgPath = './data/Radiographs/%02d.tif' % (self.radiographID + 1)
        self.image = cv2.cvtColor(cv2.imread(self.imgPath), cv2.COLOR_BGR2GRAY)
        self.downscaleImage()

        if hasLandmarks:
            for i in range(self.nb_teeth):
                landmark = self.loadLandmark('./data/Landmarks/original/' +
                                             'landmarks%d-%d.txt'
                                             % (radiographID + 1, i + 1))
                self.teeth.append(Tooth(landmark))

    def loadLandmark(self, path):

        with open(path) as landmark_file:
            landmark = np.array(landmark_file.readlines(), dtype=float)

        if landmark is not None:
            landmark = landmark.reshape((landmark.shape[0] // 2, 2))

        return landmark
    
    def downscaleImage(self, scale=0.5):
        height = self.image.shape[0]
        width = self.image.shape[1]
        self.image = cv2.resize(self.image, (int(width*scale), int(height*scale)))

    def getImage(self):
        return self.image
