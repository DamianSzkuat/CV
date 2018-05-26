from copy import deepcopy


class CompleteStatisticalModel:

    def __init__(self, statisticalToothModels, grayLevelMultiResolutionModel):
        self.statisticalToothModels = statisticalToothModels
        self.grayLevelMultiResolutionModel = grayLevelMultiResolutionModel

    def getAllToothModels(self, deepCopy=False):
        return deepcopy(self.statisticalToothModels) if deepCopy else self.statisticalToothModels
    
    def getToothModelByIndex(self, idx, deepCopy=False):
        return deepcopy(self.statisticalToothModels[idx]) if deepCopy else self.statisticalToothModels[idx]

    def getGrayLevelMultiResolutionModel(self, deepCopy=False):
        return deepcopy(self.grayLevelMultiResolutionModel) if deepCopy else self.grayLevelMultiResolutionModel
