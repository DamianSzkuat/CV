import numpy as np


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
        dXa = np.abs(dX)
        dYa = np.abs(dY)

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
        (x_1, y_1) = previous_point
        (x_2, y_2) = next_point
        (x_3, y_3) = current_point

        r = (y_2 - y_1)/(x_2 - x_1)
        b = y_3 + (1/r)*x_3

        x = x_3 + dx
        y = (-1/r)*x + b 

        return [x, y]

         
