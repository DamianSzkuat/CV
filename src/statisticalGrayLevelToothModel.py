from copy import deepcopy


class StatisticalGrayLevelToothModel:

    def __init__(self, grayLevelPointModels):
        self.grayLevelPointModels = grayLevelPointModels

    def getAllGrayLevelPointModels(self, deepCopy=False):
        return deepcopy(self.grayLevelPointModels) if deepCopy else self.grayLevelPointModels

    def getGrayLevelPointModelByIndex(self, idx, deepCopy=False):
        return deepcopy(self.grayLevelPointModels[idx]) if deepCopy else self.grayLevelPointModels[idx]