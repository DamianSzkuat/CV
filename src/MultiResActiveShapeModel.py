import numpy as np 
import math
from copy import deepcopy
import cv2

from src.PCA import PCA
from src.procrustes import Procrustes
from src.tooth  import Tooth
from src.utils import Utils
from src.filter import Filter
from src.completeStatisticalModel import CompleteStatisticalModel
from src.statisticalToothModel import StatisticalToothModel


class MultiResolutionActiveShapeModel:

    def __init__(self, completeStatisticalModel, resolutionLevels=3, m_pixels=None, k_pixels=None, filter_settings=None, initialPositions=None, initialRotations=None):
        self.completeStatisticalModel = completeStatisticalModel
        self.procrustes = Procrustes()
        self.pca = PCA()    
        self.m_pixels = m_pixels
        self.k_pixels = k_pixels
        self.resolutionLevels = resolutionLevels
        self.initialRotations = initialRotations
        self.initialPositions = self._prepareScaledInitialPositions(initialPositions)
        self.filter_settings = filter_settings
        
    
    def fitCompleteModel(self, radiograph):
        # initialize
        downscaledRadiographs = self._prepareScaledRadiographs(radiograph)

        return self._fitTeethAtMultiResolutionLevel(downscaledRadiographs)

    def _fitTeethAtMultiResolutionLevel(self, downscaledRadiographs):
        fittedModels = list()

        for i in range(8):
            toothIndex = i
            X, Y = self._fitToothAtMultiResolutionLevel(toothIndex, downscaledRadiographs)

            # test
            Y.scale(0.4)
            #print("Fitted Models: ")
            #print("Y: " + str(Y.getLandmarks()))
            #print("X: " + str(X.getLandmarks()))

            fittedModels.append([X, Y])

        return np.array(fittedModels)

    def _fitToothAtMultiResolutionLevel(self, toothIndex, downscaledRadiographs):

        # Current resolution level 
        currentResolutionLevel = self.resolutionLevels-1
        # print("Downscaled radiographs: " + str(downscaledRadiographs.shape))
        radiograph = downscaledRadiographs[currentResolutionLevel]

        # Get initial model rotations
        initialModelRotation = self.initialRotations[toothIndex]

        # Get the initial model positions
        initialModelPosition = self.initialPositions[toothIndex]
        if initialModelPosition is None:
            # Automatic model initialization not implemented
            return None
        
        # Get the mean model for the tooth
        statisticalToothModel = self.completeStatisticalModel.getToothModelByIndex(toothIndex, deepCopy=False)
        mean = Tooth(statisticalToothModel.getMeanModel())
        eigenvectors = statisticalToothModel.getEigenvectors()
        eigenvalues = statisticalToothModel.getEigenvalues()

        # Initialize Y, this has to be better
        Y = deepcopy(mean)
        Y.rotate(initialModelRotation*(math.pi/180))
        Y.scale(500/(2**(self.resolutionLevels-1)))
        #Y.scale(200)
        Y.translate(initialModelPosition)

        # print("Initialized Y: " + str(Y.getLandmarks()))

        # Init algorithm 
        b = 0
        X = mean

        while currentResolutionLevel >= 0:

            X, Y = self._fitSingleToothModel(toothIndex, currentResolutionLevel, radiograph, X, Y, b,
                                             eigenvalues, eigenvectors, mean, self.filter_settings[currentResolutionLevel])

            # print("Upscaling")
            
            # print("Changing resolution level")
            # print("X = " + str(X.getLandmarks()))
            # print("Y = " + str(Y.getLandmarks()))

            currentResolutionLevel -= 1
            if currentResolutionLevel >= 0:
                Y.scale(2)
                radiograph = downscaledRadiographs[currentResolutionLevel]

        return X, Y

    def _fitSingleToothModel(self, toothIndex, currentResolutionLevel, radiograph, X, Y, b, eigenvalues, eigenvectors, mean, filter_settings):

        scale = 500/((2*currentResolutionLevel)+1)

        Y_copy = deepcopy(Y)
        i = 0
        while i < 100:

            X, b_new = self._modelFittingStep(Y, X, eigenvalues, eigenvectors, mean, scale)
            # print("X Step: " + str(X.getLandmarks()))

            # Calculate new Y from the current X
            # I might need to first allign model X to Y, as X could still be at the origin and with no scale and rotation
            temp = self.procrustes.allignModelToData(deepcopy(Y_copy), deepcopy(X))[1]
            # print("Temp step: " + str(temp.getLandmarks()))

            Y, p = self._getNewYEstimateAtCurrentResolutionLevel(temp, radiograph, toothIndex, currentResolutionLevel, filter_settings)
            Y = Tooth(Y)
            Y_copy = deepcopy(Y)

            # if ((np.isclose(b, b_new).all() and i>3) or (i>=(12/(currentResolutionLevel+1)) and currentResolutionLevel > 0)):
            #     print("Breaking after " + str(i) + " iterations")
            #     break
            # else:
            #     b = b_new
            #     i += 1

            if (p >=0.9 and i>2)  or i >= 5:
                print("Breaking after " + str(i) + " iterations")
                break
            else:
                b = b_new
                i += 1
              
        return X, Y

    def _modelFittingStep(self, Y, X, eigenvalues, eigenvectors, mean, scale):

        # Fit Y to X
        Y_new = self.procrustes.allignDataToModel(Y,X)

        # Project Y into X space and get new b
        b = self.pca.project(Y_new.getLandmarks().flatten(), eigenvectors, mean.getLandmarks().flatten())
        # print("b = " + str(b))

        # Enforce constraint |b_i| < 3*lambda_i
        for i in range(len(b)):
            if abs(b[i]) > 2*eigenvalues[i]*scale:
                b[i] = 2*eigenvalues[i]*scale
                # print("eigenvalue: " + str(eigenvalues[i]))

        # Generate new model points X 
        X_new = self.pca.reconstruct(b, eigenvectors, mean.getLandmarks().flatten())

        X_new = X_new.reshape((X_new.shape[0] // 2, 2))

        return Tooth(X_new), b

    def _getNewYEstimateAtCurrentResolutionLevel(self, X, radiograph, currentTooth, currentResolutionLevel, filter_settings):
        # Pre process image
        img = Filter.process_image(deepcopy(radiograph.getImage(deepCopy=True)), filter_settings[0], filter_settings[1], filter_settings[2])
        derivate_img = Filter.laplacian(img)
        # derivate_img = Filter.histogramEql(Filter.process_image(deepcopy(img), filter_settings[0], filter_settings[1], filter_settings[2]))
        # derivate_img = Filter.process_image(deepcopy(derivate_img), median_kernel=3, bilateral_kernel=5)
        #cv2.imshow("Test", derivate_img)
        #cv2.waitKey(0)

        # Get the correct model
        multiResModel = self.completeStatisticalModel.getGrayLevelMultiResolutionModel(deepCopy=True)
        singleResModel = multiResModel.getGrayLevelSignleResModelByResolutionLevelIndex(currentResolutionLevel)
        toothModel = singleResModel.getGrayLevelToothModelByToothIndex(currentTooth, currentResolutionLevel)

        # Init X and Y
        Y = np.zeros((40,2))
        X = X.getLandmarks()

        counter = 0
        for i in range(40):
            Y[i], is_close = self._getYPointEstimateFromGivenModelPoint(toothModel, i,X, currentResolutionLevel,
                                                              currentTooth, img, derivate_img)
            if is_close:
                counter += 1

        return Y, counter/40

    def _getYPointEstimateFromGivenModelPoint(self, toothModel, currentPointIndex, X,
                                              currentResolutionLevel, currentTooth, img, derivate_img):

        # Get the points
        current_point = X[currentPointIndex]
        if currentPointIndex == 0:
            previous_point = X[len(X)-1]
        else:
            previous_point = X[currentPointIndex-1]
        if currentPointIndex == len(X)-1:
            next_point = X[0]
        else: 
            next_point = X[currentPointIndex+1]

        # Get the correct model
        pointModel = toothModel.getGrayLevelPointModelByIndex(currentPointIndex, currentTooth, currentResolutionLevel)
        pointMeanGrayLevels = pointModel.getMeanGrayLevels(currentTooth, currentPointIndex)
        pointCovarianceMatrix = pointModel.getCovarianceOfGrayLevels(currentTooth, currentPointIndex)

        # Get the sample from the image
        fullSampleValues, originalPixels,_ = self._getSampleAroundModelPoint(img, derivate_img, current_point, previous_point, next_point, currentResolutionLevel)

        # print("Value Samples: " + str(fullSampleValues.shape))
        # print("original Pixels: " + str(originalPixels.shape))

        # print("fullSampleValues: " + str(len(fullSampleValues)))
        # print("originalPixels: " + str(len(originalPixels)))

        # Check which slice of the sample corresponds best to the model
        bestFitValue = math.inf
        indexOfBestpoint = 0
        for i in range(len(fullSampleValues)-(2*self.k_pixels[currentResolutionLevel])):
            j = i + (2*self.k_pixels[currentResolutionLevel]) + 1
            slicedSample = fullSampleValues[i:j]
            newFitValue = self.fitFunction(slicedSample, pointMeanGrayLevels, pointCovarianceMatrix)
            if newFitValue < bestFitValue:
                bestFitValue = newFitValue
                indexOfBestpoint = i + self.k_pixels[currentResolutionLevel]

        is_close = False
        if indexOfBestpoint > len(fullSampleValues)/4 and indexOfBestpoint < (3*len(fullSampleValues))/4:
            is_close = True

        # Pick the best point
        point = originalPixels[indexOfBestpoint][:2]

        return point, is_close

    def fitFunction(self, sampleSlice, pointMeanGrayLevels, pointCovarianceMatrix):
        diff = (sampleSlice - pointMeanGrayLevels)
        diff_T = np.reshape(diff, (1,len(diff)))
        # print("Covariance matrix: " + str(pointCovarianceMatrix))
        try: 
            cov_inv = np.linalg.inv(pointCovarianceMatrix)
        except Exception:
            cov_inv = pointCovarianceMatrix
        temp = np.matmul(diff_T, cov_inv)
        distance = np.matmul(temp, diff)
        return distance 

    def _getSampleAroundModelPoint(self, img, derivate_img, current_point, previous_point, next_point, currentResolutionLevel):
        return Utils.getSampleFromImage(img, derivate_img, current_point, previous_point, next_point, self.m_pixels[currentResolutionLevel])

    def _prepareScaledRadiographs(self, radiograph):
        downscaledRadiographs = list()
        for i in range(self.resolutionLevels):
            temp = deepcopy(radiograph)
            for j in range(i):
                temp.downScale()
            downscaledRadiographs.append(temp)
        downscaledRadiographs = np.array(downscaledRadiographs)
        return downscaledRadiographs

    def _prepareScaledInitialPositions(self, initialPositions):
        if initialPositions is None:
            print("Automatic position initialisation is not implemented")
            return None
        
        scaledInitialPositions = list()
        for initialPosition in initialPositions:
            [x, y] = initialPosition

            for i in range(1, self.resolutionLevels):
                [x, y] = [x/2, y/2]
            scaledInitialPositions.append([x, y])
        scaledInitialPositions = np.array(scaledInitialPositions)
        return scaledInitialPositions

            