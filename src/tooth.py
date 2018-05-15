import numpy as np


class Tooth():

    def __init__(self, landmarks):
        self.landmarks = landmarks
        self.center = self.calculateCenter()

    def calculateCenter(self):
        self.center = np.mean(self.landmarks, axis=0)

    def downscale(self, scale):
        self.landmarks *= scale
        self.calculateCenter()

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
