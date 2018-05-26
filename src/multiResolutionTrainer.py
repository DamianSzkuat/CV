import numpy as np
import cv2
from copy import deepcopy

from src.dataHandler import DataHandler
from src.filter import Filter
from src.utils import Utils

from src.statisticalGrayLevelPointModel import StatisticalGrayLevelPointModel
from src.statisticalGrayLevelToothModel import StatisticalGrayLevelToothModel
from src.statisticalGrayLevelSingleResModel import StatisticalGrayLevelSingleResModel
from src.statisticalGrayLevelMultiResModel import StatisticalGrayLevelMultiResModel

import time 


class MultiResolutionTrainer:

    def __init__(self):
        self.completeDataHandler = DataHandler()
        self.grayLevelToothModels = None

    def trainGrayLevelMultiResolutionModel(self, k_pixels, resolutionLevels, filter_settings):
        singleResolutionModels = list()
        for i in range(resolutionLevels):
            start_time = time.time()
            singleResModel = self.trainGrayLevelSingleResolutionModel(k_pixels[i], i, filter_settings[i])
            singleResolutionModels.append(singleResModel)
            print("--- %s seconds ---" % (time.time() - start_time))
        singleResolutionModels = np.array(singleResolutionModels)
        print(str(len(singleResolutionModels)) + " single resolution models created")
        return StatisticalGrayLevelMultiResModel(singleResolutionModels, resolutionLevels)

    def trainGrayLevelSingleResolutionModel(self, k_pixels, resolutionLevel, filter_settings):
        """
        Learns the statistical gray-level models for all point on all teeth for a single resolution level 
        """
        g_all = self.trainGrayLevelModelForAllPointsAllExamples(k_pixels, resolutionLevel, filter_settings)
        print("g_all: " + str(g_all.shape))
        grayLevelToothModels = self.trainGrayLevelToothModels(g_all, k_pixels, resolutionLevel)

        print(str(len(grayLevelToothModels)) + " Gray level tooth models created during training")

        return StatisticalGrayLevelSingleResModel(grayLevelToothModels, resolutionLevel)

    def trainGrayLevelToothModels(self, g_all, k_pixels, resolutionLevel):
        grayLevelToothModels = list()
        for i in range(8):
            grayLevelPointModels = list()
            for j in range(40):
                g_point = list()
                for k in range(14):
                    g_point.append(g_all[k][i][j])
                g_point = np.array(g_point)
                g_point_mean = np.mean(g_point, axis=0)
                g_point_cov = np.cov(g_point.T)
                grayLevelPointModels.append(StatisticalGrayLevelPointModel(g_point_mean, g_point_cov, k_pixels, i, j))
            grayLevelPointModels = np.array(grayLevelPointModels)
            statisticalGrayLevelToothModel = StatisticalGrayLevelToothModel(grayLevelPointModels, i, resolutionLevel)
            grayLevelToothModels.append(statisticalGrayLevelToothModel)

        return np.array(grayLevelToothModels)
                    
    def trainGrayLevelModelForAllPointsAllExamples(self, k, resolutionLevel, filter_settings):
        """
        calcualtes the gray-level vectors for all point of all teeth in all provided examples.
        """
        radiographs = self.completeDataHandler.getRadiographs(deepCopy=True)

        g_all = list()
        for radiograph in radiographs:
            
            # Scale image to current resolution level
            for i in range(resolutionLevel):
                radiograph.downScale()

            # Pre process image
            img = radiograph.getImage(deepCopy=True)
            # print("Size trained image: " + str(img.shape))
            derivate_img = Filter.cannyEdge(Filter.process_image(deepcopy(img), filter_settings[0], filter_settings[1], filter_settings[2]))
            # derivate_img = Filter.process_image(deepcopy(derivate_img), median_kernel=3, bilateral_kernel=5)
            
            g_ex = self.trainGrayLevelModelForAllPointsOneExample(img, derivate_img, radiograph, k)
            g_all.append(g_ex)
        
        return np.array(g_all)

    def trainGrayLevelModelForAllPointsOneExample(self, img, derivate_img, radiograph, k):
        """
        Calculate the grey-level vectors for all points of all teeth in one example.
        """
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
                
                g_p.append(self.trainGrayLevelModelForOnePointOneExample(img, derivate_img, current_point, previous_point, next_point, k))
            g_ex.append(np.array(g_p))
        
        return np.array(g_ex)

    def trainGrayLevelModelForOnePointOneExample(self, img, derivate_img, current_point, previous_point, next_point, k):
        """
        calculates the grey-level vector of the pixels on the normal in the given point in the given example.
        """
        sample,_,_ = Utils.getSampleFromImage(img, derivate_img, current_point, previous_point, next_point, k)
        return sample