import numpy as np
from copy import deepcopy
import math

from src.dataHandler import DataHandler
from src.procrustes import Procrustes
from src.PCA import PCA
from src.modelFitter import ModelFitter
from src.filter import Filter
from src.utils import Utils
from src.multiResolutionTrainer import MultiResolutionTrainer

from src.statisticalToothModel import StatisticalToothModel
from src.completeStatisticalModel import CompleteStatisticalModel


class StatisticalModelTrainer:

    def __init__(self):
        self.completeDataHandler = DataHandler()
        self.procrustes = Procrustes()
        self.pca = PCA()
        self.modelFitter = ModelFitter()
        self.multiResTrainer = MultiResolutionTrainer()

    def trainCompleteStatisticalModel(self, k_pixels, resolutionLevels, filter_settings, doLeaveOneOutTrainingSetTest=False, leaveOneOut=None):
        """
        Performs leave-one-out validation of the training set, then 
        trains a statistical model from the entire training set.
        """
        if doLeaveOneOutTrainingSetTest:
            self.doLeaveOneOutTrainingSetValidation()

        if leaveOneOut is not None:
            self.completeDataHandler = DataHandler(leave_one_out=leaveOneOut)
            
        statisticalToothModels = self.trainModelFromCompleteTrainingSet()

        grayLevelMultiResModel = self.multiResTrainer.trainGrayLevelMultiResolutionModel(k_pixels, resolutionLevels, filter_settings)

        completeModel = CompleteStatisticalModel(statisticalToothModels, grayLevelMultiResModel)

        print("Statistical model trained!")

        return completeModel
    
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
        return meanModels

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
        