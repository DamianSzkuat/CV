from src.radiograph import Radiograph
from copy import deepcopy


class DataHandler:

    def __init__(self, leave_one_out=None):
        self.radiographs = list()
        self.nb_radiographs = 14

        for i in range(self.nb_radiographs):
            radiograph = Radiograph()
            radiograph.loadRadiograph(i, True)

            if leave_one_out is not None and i == leave_one_out:
                self.left_out_radiograph = radiograph
                continue

            self.radiographs.append(radiograph)

    def getLeftOutRadiograph(self, deepCopy=False):
        return deepcopy(self.left_out_radiograph) if deepcopy else self.radiographs

    def getAllTeethSets(self, deepCopy=False):
        teethSets = list()
        for radiograph in self.radiographs:
            teethSets += [(radiograph.getTeethSet(deepCopy=deepCopy))]
        return teethSets

    def getAllTeeth(self, deepCopy=False):
        teeth = list()
        for radiograph in self.radiographs:
            teeth += (radiograph.getTeeth(deepCopy=deepCopy))
        return teeth

    def getAllUpperTeeth(self, deepCopy=False):
        teeth = list()
        for radiograph in self.radiographs:
            teeth += (radiograph.getUpperTeeth(deepCopy=deepCopy))
        return teeth

    def getAllLowerTeeth(self, deepCopy=False):
        teeth = list()
        for radiograph in self.radiographs:
            teeth += (radiograph.getLowerTeeth(deepCopy=deepCopy))
        return teeth

    def getAllTeethAtIndex(self, idx, deepCopy=False):
        teeth = list()
        for radiograph in self.radiographs:
            teeth += [(radiograph.getTeethAtIndex(idx, deepCopy=deepCopy))]
        return teeth

    def getRadiographs(self, deepCopy=False):
        return deepcopy(self.radiographs) if deepCopy else self.radiographs

    def getNBofRadiographs(self):
        return self.nb_radiographs
