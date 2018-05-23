import numpy as np


class Tooth():

    def __init__(self, landmarks):
        self.landmarks = landmarks
        self.calculateCenter()

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
        print("Normalized Landmarks: " + str(self.landmarks))
        print("Norm of these landmarks: " + str(np.linalg.norm(self.landmarks)))
        self.calculateCenter()

    def getLandmarks(self):
        return self.landmarks

    def getCenter(self):
        return self.center
