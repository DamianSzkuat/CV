import numpy as np


class PCA:

    def do_pca_and_build_model(self, teeth):
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

        return [mean, eigenvalues, eigenvectors]

    def pca(self, X, number_of_components):
        # mean
        mean = np.mean(X, axis=0)

        X -= mean

        # SVD
        _, S, V = np.linalg.svd(X, full_matrices=True)

        eigenvalues = S[0:number_of_components]
        eigenvectors = V[:, 0:number_of_components]

        return [mean, eigenvalues, eigenvectors]

    def get_image_from_vector(self, vector, shape):
        M = vector

        img = np.reshape(M, shape, order='A')

        return img
