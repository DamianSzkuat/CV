from copy import deepcopy


class CompleteStatisticalModel:

    def __init__(self, statisticalToothModels, statisticalGrayLevelToothModels=None):
        self.statisticalToothModels = statisticalToothModels
        self.statisticalGrayLevelToothModels = statisticalGrayLevelToothModels

    def getAllToothModels(self, deepCopy=False):
        return deepcopy(self.statisticalToothModels) if deepCopy else self.statisticalToothModels
    
    def getToothModelByIndex(self, idx, deepCopy=False):
        return deepcopy(self.statisticalToothModels[idx]) if deepCopy else self.statisticalToothModels[idx]

    def getAllGrayLevelToothModels(self, deepCopy=False):
        return deepcopy(self.statisticalGrayLevelToothModels) if deepCopy else self.statisticalGrayLevelToothModels

    def getGrayLevelToothModelByIndex(self, idx, deepCopy=False):
        return deepcopy(self.statisticalGrayLevelToothModels[idx]) if deepcopy else self.statisticalGrayLevelToothModels[idx]
