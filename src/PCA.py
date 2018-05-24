import numpy as np


class PCA:

    def do_pca_and_build_model(self, teeth):
        """
        Performs pca on the provided examples and return a statistical model.
        """
        N = len(teeth)
        P = teeth[0].getLandmarks().shape[0]*teeth[0].getLandmarks().shape[1]
        X = np.zeros((N, P))
        for i in range(len(teeth)):

            data = teeth[i].getLandmarks()
            v = data.flatten()
            for j in range(len(v)):
                X[i][j] = v[j]

        mean, eigenvalues, eigenvectors = self.pca(X, number_of_components=N)
        mean = self.get_image_from_vector(mean, teeth[0].getLandmarks().shape)
        totalVariance = self.getTotalVariance(eigenvalues)
        importantEigenvalues, importantEigenvectors = self.getKLangestEigenvalues(eigenvalues, eigenvectors, totalVariance)
        return [mean, importantEigenvalues, importantEigenvectors]

    def pca(self, X, number_of_components):
        """
        Performs principal components analysis
        """
        [n,d] = X.shape
        
        mean = np.mean(X, axis=0)

        X -= mean

        if n > d:
            C = np.dot(X.T, X) / (X.shape[0] - 1)
            [eigenvalues, eigenvectors] = np.linalg.eigh(C)
        else:
            C = np.dot(X, X.T) / (X.shape[1] - 1)
            [eigenvalues, eigenvectors] = np.linalg.eigh(C)
            eigenvectors = np.dot(X.T, eigenvectors)
            for i in range(n):
                eigenvectors[:, i] = eigenvectors[:, i] / np.linalg.norm(eigenvectors[:, i])

        idx = np.argsort(-eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        eigenvalues = eigenvalues[0:number_of_components].copy()
        eigenvectors = eigenvectors[:, 0:number_of_components].copy()

        return [mean, eigenvalues, eigenvectors]

    def project(self, vector, eigenvectors, mean=None):
        if mean is None:
            return np.dot(vector, eigenvectors)

        projection = np.dot(vector-mean, eigenvectors)
        return projection

    def reconstruct(self, param, eigenvectors, mean=None):
        if mean is None:
            return np.dot(param, eigenvectors.T)
        return np.dot(param, eigenvectors.T) + mean

    def get_image_from_vector(self, vector, shape):
        M = vector
        img = np.reshape(M, shape, order='A')
        return img

    def getTotalVariance(self, eigenvalues):
        return np.sum(eigenvalues)

    def getKLangestEigenvalues(self, eigenvalues, eigenvectors, totalVariance):
        importantEigenvalues = [eigenvalues[0]]

        i = 0
        while np.sum(importantEigenvalues)/totalVariance < 0.99:
            i += 1
            importantEigenvalues.append(eigenvalues[i])

        importantEigenvectors = eigenvectors[:,:i+1]

        return importantEigenvalues, importantEigenvectors
        
