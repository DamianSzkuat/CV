You can start the gui with the command: python main.py 

The code is set up so that the first image you see (radiograph number 0) will be the radiograph that is left out from the training set, 
and can be used as a test image. If you want to change that you can go to main.py line 93:
"self.statisticalModel = self.statisticalModelTrainer.trainCompleteStatisticalModel(self.k_pixels, self.resolutionLevels, self.filter_settings, leaveOneOut=0)"
and change the leaveOneOut value to any number between 0 and 13.

---------
Gui
---------

When you start the gui you will see a picture of radiograph 0 with the landmarks drawn on it. 
Right of the image are several buttons:

* Next Image & Previous image are pretty self explanatory, you can toggle images

* Train complete statistical model: This will train the pca and gray-level model. You have to do this every time you start the gui anew. 

* Manual position inialization: Once the model is trained you can fit it to the test image. When you press this button an image of radiograph 0 will appear once again but without the landmarks. You can toggle the image like before to chose the one you want to fit the model to, preferably the test image.

-> pres the left mouse button on the image to place a tooth. You can keep pressing the left mouse button to move the tooth model to a better spot. 
-> drag the scale left and right to rotate the model. You can alternate between moving the model and rotating it.
-> when you are happy with the model placement press the "Accept model position" button. This will fix the position of the current tooth model and allow you to place the next model. Models are places left to right, top incisors first, then bottom. Don't forget to press "accept model position" after the last tooth model is placed. 

* Automatic position initialization: This is not implemented and will do nothing

* Model fitting: the model will be fit the the radiograph. Once the fitting is done the gui will display the resulting fit and a new window will open showing the comparison of the fit to the original landmakrs. in this comparison the blue contour is the fitted model, the green contour are the original landmarks and the red lines connect the corresponding points of both contours. 



