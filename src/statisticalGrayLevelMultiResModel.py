from copy import deepcopy


class StatisticalGrayLevelMultiResModel:

    def __init__(self, grayLevelSignleResModels, nb_resolutionlevels):

        self.nb_resolutionlevels = nb_resolutionlevels
        self.grayLevelSignleResModels = grayLevelSignleResModels

    def getAllGrayLevelSingleResModels(self, deepCopy=False):
        return deepcopy(self.grayLevelSignleResModels) if deepCopy else self.grayLevelSignleResModels
    
    def getGrayLevelSignleResModelByResolutionLevelIndex(self, resolutionLevel, deepCopy=False):
        return deepcopy(self.grayLevelSignleResModels[resolutionLevel]) if deepCopy else self.grayLevelSignleResModels[resolutionLevel]