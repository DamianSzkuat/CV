import numpy as np
from copy import deepcopy


from src.dataHandler import DataHandler
from src.procrustes import Procrustes
from src.PCA import PCA
from src.modelFitter import ModelFitter
from src.filter import Filter
from src.utils import Utils

from src.statisticalToothModel import StatisticalToothModel
from src.completeStatisticalModel import CompleteStatisticalModel


class StatisticalModelTrainer:

    def __init__(self):
        self.completeDataHandler = DataHandler()
        self.procrustes = Procrustes()
        self.pca = PCA()
        self.modelFitter = ModelFitter()

    def trainCompleteStatisticalModel(self, doLeaveOneOutTrainingSetTest=False):
        """
        Performs leave-one-out validation of the training set, then 
        trains a statistical model from the entire training set.
        """
        if doLeaveOneOutTrainingSetTest:
            self.doLeaveOneOutTrainingSetValidation()
        statisticalModel = self.trainModelFromCompleteTrainingSet()
        print("Statistical model trained!")

        #TEST
        radiograph = self.completeDataHandler.getRadiographs()[0]
        k = 2
        g_ex = self.calculateGrayLevelModelForAllPointsOneExample(radiograph, k)
        print("g_ex.shape = " + str(g_ex.shape))

        return statisticalModel
    
    def trainModel(self, dataHandler):
        """
        Trains a statistical model from the examples provided in the given dataHandler.
        """
        alignedTrainingExamples = self.allignTrainingExamples(dataHandler)
        return self.perfromPCA(alignedTrainingExamples)

    def allignTrainingExamples(self, dataHandler):
        """
        Alligns all training examples, grouped by the same tooth, using procrustes analysis.
        """
        alignedTrainingExamples = list()
        for i in range(8):
            temp = dataHandler.getAllTeethAtIndex(i, deepCopy=True)
            alignedTrainingExamples.append(self.procrustes.performProcrustesAlignment(temp))
        return alignedTrainingExamples

    def perfromPCA(self, alignedTrainingExamples):
        """
        Performs PCA on the given training set, and returns the obtained statistical models.
        """
        meanModels = list()
        for i in range(8):
            [mean, eigenvalues, eigenvectors] = self.pca.do_pca_and_build_model(alignedTrainingExamples[i])
            statisticalToothModel = StatisticalToothModel(mean, eigenvalues, eigenvectors)
            meanModels.append(statisticalToothModel)
        meanModels = np.array(meanModels)
        completeStatisticalModel = CompleteStatisticalModel(meanModels)
        return completeStatisticalModel
    
    def calculateGrayLevelModelForAllPointsOneExample(self, radiograph, k):
        g_ex = list()

        teeth = radiograph.getTeeth()
        for tooth in teeth:
            points = tooth.getLandmarks()
            g_p = list()
            for i in range(len(points)):
                current_point = points[i]
                
                if i == 0:
                    previous_point = points[len(points)-1]
                else:
                    previous_point = points[i-1]
                
                if i == len(points)-1:
                    next_point = points[0]
                else: 
                    next_point = points[i+1]
                
                g_p.append(self.calculateGrayLevelModelForOnePointOneExample(radiograph, current_point, previous_point, next_point, k))
            g_ex.append(np.array(g_p))
        
        return np.array(g_ex)

    def calculateGrayLevelModelForOnePointOneExample(self, radiograph, current_point, previous_point, next_point, k):
        """
        calculates the grey-level vector of the pixels on the normal in the given point in the given example.
        """

        derivate_img = Filter.process_image(radiograph.getImage(deepCopy=True))
        img = radiograph.getImage(deepCopy=True)

        [x_1, y_1] = Utils.getPointOnNormal(current_point, previous_point, next_point, k)
        [x_2, y_2] = Utils.getPointOnNormal(current_point, previous_point, next_point, -k)

        originalPixels = Utils.createLineIterator([np.float32(x_1), np.float32(y_1)], [np.float32(x_2), np.float32(y_2)], img)
        derivatePixels = Utils.createLineIterator([np.float32(x_1), np.float32(y_1)], [np.float32(x_2), np.float32(y_2)], derivate_img)

        print("Point: " + str(current_point))
        print("Original pixels: " + str(originalPixels))
        # print("derivative pixels: " + str(derivatePixels))

        if len(originalPixels) > 2*k + 1:
            i = Utils.getIndexOfClosestPixelInArray(current_point, originalPixels)
            print("Returned index = " + str(i))
            originalPixels = originalPixels[i-k:i+k+1][:]
            
        if len(derivatePixels) > 2*k + 1:
            i = Utils.getIndexOfClosestPixelInArray(current_point, originalPixels)
            originalPixels = originalPixels[i-k:i+k+1][:]

        # TODO what if not enough pixels taken!!

        g = derivatePixels / np.sum(originalPixels)

        return g

    def trainModelFromCompleteTrainingSet(self):
        """
        Trains a statistical model from the complete training set.
        """
        statisticalModel = self.trainModel(self.completeDataHandler)
        return statisticalModel

    def doLeaveOneOutTrainingSetValidation(self):
        """
        Performs a leave-one-out validation of the training set. 
        If for any subset of the training set the error on the leaft out example
        is too big, the training set is considered insuficient.
        """
        # Number of training examples
        n = len(self.completeDataHandler.getRadiographs(deepCopy=True))

        for i in range(n):
            dataHandler = DataHandler(leave_one_out=i)
            statisticalModel = self.trainModel(dataHandler)
            self.testTrainedModelOnLeftOutExample(dataHandler, statisticalModel)
        
    def testTrainedModelOnLeftOutExample(self, dataHandler, statisticalModel):
        """
        Test the learned model by fitting it to the train examples as well as to the
        left out exampele and compares the mean error on the training examples to the 
        error on the left out example.
        """

        training_radiographs = dataHandler.getRadiographs(deepCopy = True)
        leftOut_radiograph = dataHandler.getLeftOutRadiograph(deepCopy = True)

        total_error = 0
        for radiograph in training_radiographs:
            error = self.fitModelToAnnotatedExampleAndMeasureError(radiograph, statisticalModel)
            total_error += error
        errorOnTrainingExamples = total_error / len(training_radiographs)

        errorOnLeftOutExample = self.fitModelToAnnotatedExampleAndMeasureError(leftOut_radiograph, statisticalModel)

        errorComparison = errorOnLeftOutExample / errorOnTrainingExamples

        if errorComparison > 3:
            print("Relative error on left out example = " + str(errorOnLeftOutExample))
            print("Error on test image is relativelly big (>3 times the mean error on the train images), " +
            "the training set might not be good enough")

    def fitModelToAnnotatedExampleAndMeasureError(self, radiograph, statisticalModel):
        """
        Fits a model to an annotated example and measures the error.
        """
        teeth = radiograph.getTeeth(deepCopy=True)
        total_error = 0
        for i in range(8):
            tooth = deepcopy(teeth[i])
            model = statisticalModel.getToothModelByIndex(i, deepCopy=True)

            # Fit the model to the radiograph
            fitted_model = self.modelFitter.fitModel(deepcopy(tooth), model)

            # align fitted model to examples
            alignedModel = self.procrustes.allignModelToData(deepcopy(tooth), fitted_model)[1]

            # Error is the measured as the norm of the difference of the two matrices
            error = (tooth.getLandmarks() - alignedModel.getLandmarks())/alignedModel.getLandmarks()
            error = np.linalg.norm(error)
            total_error += error
        
        return total_error
        