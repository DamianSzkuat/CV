import numpy as np 
import math

from src.PCA import PCA
from src.procrustes import Procrustes
from src.tooth  import Tooth

class ModelFitter:

    def fitModel(self, target_tooth, model):
        
        self.procrustes = Procrustes()
        self.pca = PCA()
        eigenvalues = np.array(model[1])
        eigenvectors = np.array(model[2])
        Y = target_tooth
        mean = model[0]

        #print("Mean = " + str(mean.getLandmarks().shape))
        #print("eigenvalues = " + str(eigenvalues.shape))
        #print("eigenvectors = " + str(eigenvectors.shape))

        # Init 
        b = 0
        X = mean

        i = 0
        while i < 20:
            i += 1

            X, b_new = self.step(Y, X, eigenvectors, mean)

            print(" i = " + str(i) + ", b_new = " + str(b_new))

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

        

