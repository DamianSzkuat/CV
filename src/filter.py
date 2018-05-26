import cv2
from src.utils import Rectangle
import numpy as np


class Filter:

    @staticmethod
    def process_image(img, median_kernel=5, bilateral_kernel=17, bilateral_color=9):
        """
        Filter and image with median blurr and bilateral filter.
        """
        
        img = cv2.medianBlur(img, median_kernel)
        img = cv2.bilateralFilter(img, bilateral_kernel, bilateral_color, 50)
        return img

    # @staticmethod
    # def laplacian(img):
    #     img = cv2.Laplacian(img, cv2.CV_64F)
    #     return img

    @staticmethod
    def cannyEdge(img):
        img = cv2.Canny(img, 15, 15)
        return img

    @staticmethod
    def cropImageToRegionOfInterest(img, resolutionLevel):
        """
        Crop image to the region of interest
        """
        resLevelScale = 1/2**resolutionLevel
        h, w = img.shape
        h2, w2 = h/2, w/2
        region = Rectangle(w2 - (400*resLevelScale),
                           500*resLevelScale,
                           w2 + (400*resLevelScale),
                           1400*resLevelScale)
        return img[int(region.top):int(region.bottom), int(region.left):int(region.right)].copy()