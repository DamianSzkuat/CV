from copy import deepcopy


class StatisticalGrayLevelSingleResModel:

    def __init__(self, grayLevelToothModels, resolutionLevel):
        self.resolutionLevel = resolutionLevel
        self.grayLevelToothModels = grayLevelToothModels
        print("Single res model created with " + str(len(self.grayLevelToothModels)) + " tooth models")

    def getAllGrayLevelToothModels(self, resolutionLevel, deepCopy=False):
        if self.resolutionLevel == resolutionLevel:
            return deepcopy(self.grayLevelToothModels) if deepCopy else self.grayLevelToothModels
        else:
            print("StatisticalGrayLevelSingleResModel: Resolution level does not match!!!")
    
    def getGrayLevelToothModelByToothIndex(self, toothIndex, resolutionLevel, deepCopy=False):
        if self.resolutionLevel == resolutionLevel:
            return deepcopy(self.grayLevelToothModels[toothIndex]) if deepCopy else self.grayLevelToothModels[toothIndex] 
        else:
            print("StatisticalGrayLevelSingleResModel: Resolution level does not match!!!")