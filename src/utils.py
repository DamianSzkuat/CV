import numpy as np
import math 


class Utils:

    @staticmethod
    def createLineIterator(P1, P2, img):
        """
        Produces and array that consists of the coordinates and intensities of each pixel in a line between two points

        Parameters:
            -P1: a numpy array that consists of the coordinate of the first point (x,y)
            -P2: a numpy array that consists of the coordinate of the second point (x,y)
            -img: the image being processed

        Returns:
            -it: a numpy array that consists of the coordinates and intensities of each pixel in the radii (shape: [numPixels, 3], row = [x,y,intensity]) 

        From : https://stackoverflow.com/questions/32328179/opencv-3-0-python-lineiterator   
        """
        #define local variables for readability
        imageH = img.shape[0]
        imageW = img.shape[1]
        P1X = P1[0]
        P1Y = P1[1]
        P2X = P2[0]
        P2Y = P2[1]

        #difference and absolute difference between points
        #used to calculate slope and relative location between points
        dX = P2X - P1X
        dY = P2Y - P1Y
        dXa = Utils.ceiling(np.abs(dX))
        dYa = Utils.ceiling(np.abs(dY))

        #predefine numpy array for output based on distance between points
        itbuffer = np.empty(shape=(np.maximum(Utils.ceiling(dYa),Utils.ceiling(dXa)),3),dtype=np.float32)
        itbuffer.fill(np.nan)

        #Obtain coordinates along the line using a form of Bresenham's algorithm
        negY = P1Y > P2Y
        negX = P1X > P2X
        if P1X == P2X: #vertical line segment
            itbuffer[:,0] = P1X
            if negY:
                itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
            else:
                itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)              
        elif P1Y == P2Y: #horizontal line segment
            itbuffer[:,1] = P1Y
            if negX:
                itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
            else:
                itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
        else: #diagonal line segment
            steepSlope = dYa > dXa
            if steepSlope:
                slope = dX.astype(np.float32)/dY.astype(np.float32)
                if negY:
                    itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
                else:
                    itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
                itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(np.int) + P1X
            else:
                slope = dY.astype(np.float32)/dX.astype(np.float32)
                if negX:
                    itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
                else:
                    itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
                itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(np.int) + P1Y

        #Remove points outside of image
        colX = itbuffer[:,0]
        colY = itbuffer[:,1]
        itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]

        #Get intensities from img ndarray
        itbuffer[:,2] = img[itbuffer[:,1].astype(np.uint),itbuffer[:,0].astype(np.uint)]

        return itbuffer
    
    @staticmethod
    def ceiling(x):
        n = int(x)
        return n if n-1 < x <= n else n+1

    @staticmethod
    def getIndexOfClosestPixelInArray(point, array):
        array = array[:,:2]
        diff_array = abs(array - point)

        n = array.shape[0]
        smallest_value = 100
        smallest_value_index = 0

        for i in range(n):
            current_value = np.sum(diff_array[i])
            if current_value < smallest_value:
                smallest_value = current_value
                smallest_value_index = i

        return smallest_value_index

    @staticmethod
    def getPointOnNormal(current_point, previous_point, next_point, dx):
        (x_a, y_a) = previous_point
        (x_b, y_b) = next_point
        (x_c, y_c) = current_point

        if math.isclose(x_a, x_b):
            [x, y] = [x_c, y_c + dx]
            [x, y] = [x_c, y_c - dx]
        elif math.isclose(y_a, y_b) :
            [x, y] = [x_c + dx, y_c]
            [x, y] = [x_c - dx, y_c]
        else:    
            r = (y_b - y_a)/(x_b - x_a)
            b = y_c + (1/r)*x_c
            x = x_c + dx
            y = (-1/r)*x + b 

        return [x, y]
    
    @staticmethod
    def getSampleFromImage(img, derivate_img, current_point, previous_point, next_point, k):
        """
        Returns a sample of 2*k+1 pixels on the normal to the model in the given point.
        """

        # print("img: " + str(img.shape))
        # print("derivate_img: " + str(derivate_img.shape))
        # print("Current point: " + str(current_point))
        # print("Previous point: " + str(previous_point))
        # print("Next point: " + str(next_point))

        # Get two points on the normal to the model at the given point
        i = 1
        while True:
            [x_1, y_1] = Utils.getPointOnNormal(current_point, previous_point, next_point, (k+1)/i)
            [x_2, y_2] = Utils.getPointOnNormal(current_point, previous_point, next_point, -(k+1)/i)

            # print("Points on the normal: " + str([x_1, y_1]) + ", " + str([x_2, y_2]))

            # Get the pixels on the normal between the two given points from both images
            originalPixels = Utils.createLineIterator([np.float32(x_1), np.float32(y_1)], [np.float32(x_2), np.float32(y_2)], img)
            derivatePixels = Utils.createLineIterator([np.float32(x_1), np.float32(y_1)], [np.float32(x_2), np.float32(y_2)], derivate_img)

            # print("originalPixels.shape: " + str(originalPixels.shape))

            if originalPixels.shape[0] > 2*k: # and x_1 > 0 and y_1 > 0 and x_2 > 0 and y_2 > 0:
                break
            if i > 10:
                break
            i += 1
            break
        
        # Remove unnecessary pixels
        if len(originalPixels) > 2*k + 1:
            i = Utils.getIndexOfClosestPixelInArray(current_point, originalPixels)
            originalPixels = originalPixels[i-k:i+k+1][:]
            
        if len(derivatePixels) > 2*k + 1:
            i = Utils.getIndexOfClosestPixelInArray(current_point, derivatePixels)
            derivatePixels = derivatePixels[i-k:i+k+1][:]

        # Take only the gray values from the arrays
        originalPixelsValues = originalPixels[:,2:].flatten()
        derivatePixelsValues = derivatePixels[:,2:].flatten()

        # Divide the vector of derivate gray values by the sum of the values of the 
        # pixels from the original image.
        return derivatePixelsValues / np.sum(originalPixelsValues), originalPixels, derivatePixels

class Rectangle:
    top = None
    bottom = None
    left = None
    right = None

    def __init__(self, left, top, right, bottom):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def left_top(self):
        return np.array((self.left, self.top))
