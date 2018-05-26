from copy import deepcopy


class StatisticalGrayLevelToothModel:

    def __init__(self, grayLevelPointModels, toothIndex, resolutionLevel):
        self.resolutionLevel = resolutionLevel
        self.toothIndex = toothIndex
        self.grayLevelPointModels = grayLevelPointModels

    def getAllGrayLevelPointModels(self, toothIndex, resolutionLevel, deepCopy=False):
        if self.toothIndex == toothIndex and self.resolutionLevel == resolutionLevel:
            return deepcopy(self.grayLevelPointModels) if deepCopy else self.grayLevelPointModels
        else: 
            print("StatisticalGrayLevelToothModel: The indices dont match: self.toothindex = " + str(self.toothIndex), ", self.resolutionlevel: " + str(self.resolutionLevel))

    def getGrayLevelPointModelByIndex(self, idx, toothIndex, resolutionLevel, deepCopy=False):
        if self.toothIndex == toothIndex and self.resolutionLevel == resolutionLevel:
            return deepcopy(self.grayLevelPointModels[idx]) if deepCopy else self.grayLevelPointModels[idx]
        else: 
            print("StatisticalGrayLevelToothModel: The indices dont match: self.toothindex = " + str(self.toothIndex), ", self.resolutionlevel: " + str(self.resolutionLevel))