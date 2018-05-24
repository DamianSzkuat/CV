import cv2


class Filter:

    @staticmethod
    def process_image(img, median_kernel=5, bilateral_kernel=17, bilateral_color=9):
        """
        Filter and image with median blurr, bilateral filter and a laplacian.
        """
        img = cv2.medianBlur(img, median_kernel)
        img = cv2.bilateralFilter(img, bilateral_kernel, bilateral_color, 200)
        img = cv2.Laplacian(img, cv2.CV_64F)
        return img