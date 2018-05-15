import numpy as np

from src.tooth import Tooth


class Radiograph:
    imgPath = None
    teeth = None
    radiographID = None

    def __init__(self):
        self.teeth = list()
        self.nb_teeth = 8

    def loadRadiograph(self, radiographID, hasLandmarks=False):
        self.radiographID = radiographID
        self.imgPath = './data/Radiographs/%02d.tif' % (self.radiographID + 1)

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
