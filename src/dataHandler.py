from src.radiograph import Radiograph


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

    def getRadiographs(self):
        return self.radiographs
    
    def getNBofRadiographs(self):
        return self.nb_radiographs
