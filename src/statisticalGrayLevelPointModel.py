from copy import deepcopy


class StatisticalGrayLevelPointModel:

    def __init__(self, meanGrayLevels, covarianceOfGrayLevels, k, toothIndex, pointIndex):
        self.k = k
        self.nb_pixels = 2*k + 1
        self.toothIndex = toothIndex
        self.pointIndex = pointIndex

        if meanGrayLevels.shape == (self.nb_pixels,):
            self.meanGrayLevels = meanGrayLevels
        else:
            print("Shape of mean gray levels wrong!!")

        if covarianceOfGrayLevels.shape == (self.nb_pixels,self.nb_pixels):
            self.covarianceOfGrayLevels = covarianceOfGrayLevels
        else:
            print("Shape of covariance matrix wrong!!")

    def getMeanGrayLevels(self, toothIndex, pointIndex, deepCopy=False):
        if self.toothIndex == toothIndex and self.pointIndex == pointIndex:
            return deepcopy(self.meanGrayLevels) if deepCopy else self.meanGrayLevels
        else:
            print("StatisticalGrayLevelPointModel: The indices dont match!!!")

    def getCovarianceOfGrayLevels(self, toothIndex, pointIndex, deepCopy=False):
        if self.toothIndex == toothIndex and self.pointIndex == pointIndex:
            return deepcopy(self.covarianceOfGrayLevels) if deepCopy else self.covarianceOfGrayLevels
        else:
            print("StatisticalGrayLevelPointModel: The indices dont match!!!")