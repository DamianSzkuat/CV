import numpy as np
from sklearn.preprocessing import normalize
import math

class Procrustes:

    def __init__(self, dataHandler):
        self.teeth = dataHandler.getAllTeeth(deepCopy=True)
        self.fixedTooth = self.teeth[0]
    
    def performProcrustesAlignment(self):
        self.translateTeethToOrigin()
        self.normalizeFixedShape()
        self.scaleAndRotateShapes()
        return self.teeth

    def translateTeethToOrigin(self):
        for tooth in self.teeth:
            tooth.translate(-tooth.getCenter())
    
    def normalizeFixedShape(self):
        self.fixedTooth.normalize()

    def scaleAndRotateShapes(self):
        for i in range(len(self.teeth)):
            tooth = self.teeth[i]
            a_j = self.calculate_a_j(tooth)
            b_j = self.calculate_b_j(tooth)
            s_j = self.calculate_s_j(a_j, b_j)
            theta_j = self.calculate_theta_j(a_j, b_j)
            tooth.scale(s_j)
            tooth.rotate(theta_j)

    def calculate_a_j(self, tooth):
        temp = 0
        landmarks_1 = self.fixedTooth.getLandmarks()
        landmarks_j = tooth.getLandmarks()
        for i in range(len(landmarks_j)):
            x_j = landmarks_j[i][0]
            y_j = landmarks_j[i][1]
            x_1 = landmarks_1[i][0]
            y_1 = landmarks_1[i][1]
            temp += x_j*y_1 + x_1*y_j
        a_j = temp / (np.linalg.norm(tooth.getLandmarks()))**2
        return a_j
    
    def calculate_b_j(self, tooth):
        temp = 0
        landmarks_1 = self.fixedTooth.getLandmarks()
        landmarks_j = tooth.getLandmarks()
        for i in range(len(landmarks_j)):
            x_j = landmarks_j[i][0]
            y_j = landmarks_j[i][1]
            x_1 = landmarks_1[i][0]
            y_1 = landmarks_1[i][1]
            temp += x_j*y_1 - x_1*y_j
        b_j = temp / (np.linalg.norm(tooth.getLandmarks()))**2
        return b_j
    
    def calculate_s_j(self, a_j, b_j):
        return math.sqrt((a_j**2) + (b_j**2))
    
    def calculate_theta_j(self, a_j, b_j):
        return math.atan(b_j/a_j)



