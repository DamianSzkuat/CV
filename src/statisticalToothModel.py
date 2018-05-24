from copy import deepcopy

class StatisticalToothModel:

    def __init__(self, meanModel, eigenvalues, eigenvectors):
        self.meanModel = meanModel
        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors

    def getMeanModel(self, deepCopy=False):
        return deepcopy(self.meanModel) if deepCopy else self.meanModel

    def getEigenvalues(self, deepCopy=False):
        return deepcopy(self.eigenvalues) if deepCopy else self.eigenvalues
    
    def getEigenvectors(self, deepCopy=False):
        return deepcopy(self.eigenvectors) if deepCopy else self.eigenvectors