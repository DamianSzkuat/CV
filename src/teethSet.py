import numpy as np

from src.tooth import Tooth


class TeethSet:

    def __init__(self, teeth):
        self.teeth = teeth
        self.landmarks = self.getConcatenatedLandmarks()
        self.center = None
        self.calculateCenter()

    def getConcatenatedLandmarks(self):
        teethSet = self.teeth[0].getLandmarks()

        for i in range(1,8):
            teethSet = np.concatenate((teethSet, self.teeth[i].getLandmarks()))
        
        return teethSet

    def calculateCenter(self):
        self.center = np.mean(self.landmarks, axis=0)

    def scale(self, scale):
        self.landmarks *= scale
        self.calculateCenter()

    def rotate(self, theta):
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, s), (-s, c)))
        temp = self.landmarks.transpose()
        temp = np.dot(R, temp)
        self.landmarks = temp.transpose()

    def translate(self, vec):
        self.landmarks += vec
        self.calculateCenter()

    def normalize(self):
        self.landmarks = self.landmarks / np.linalg.norm(self.landmarks)
        self.calculateCenter()

    def getLandmarks(self):
        return self.landmarks

    def getCenter(self):
        return self.center