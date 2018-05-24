import numpy as np 
import math

from src.PCA import PCA
from src.procrustes import Procrustes
from src.tooth  import Tooth

class ModelFitter:

    def fitModel(self, target_tooth, model):
        
        self.procrustes = Procrustes()
        self.pca = PCA()
        eigenvectors = model.getEigenvectors()
        Y = target_tooth
        mean = Tooth(model.getMeanModel())

        # Init 
        b = 0
        X = mean

        i = 0
        while i < 20:
            i += 1

            X, b_new = self.step(Y, X, eigenvectors, mean)

            if np.allclose(b, b_new):
                break
            else:
                b = b_new
   
        return X
            
    def step(self, Y, X, eigenvectors, mean):

        # Fit Y to X
        Y_new = self.procrustes.allignDataToModel(Y,X)

        # Project Y into X space and get new b
        b = self.pca.project(Y_new.getLandmarks().flatten(), eigenvectors, mean.getLandmarks().flatten())
        # print("b = " + str(b))

        # Generate new model points X 
        X_new = self.pca.reconstruct(b, eigenvectors, mean.getLandmarks().flatten())

        X_new = X_new.reshape((X_new.shape[0] // 2, 2))

        return Tooth(X_new), b

        

