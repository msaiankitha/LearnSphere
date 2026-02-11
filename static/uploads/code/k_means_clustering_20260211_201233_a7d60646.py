"""
===============================================================================
ML Learning Assistant - Generated Code
Topic: k means clustering
Generated on: 2026-02-11 20:12:33

DEPENDENCIES:
pip install matplotlib
pip install numpy
pip install scikit-learn

INSTRUCTIONS:
1. Install required dependencies using pip
2. Run this script in your Python environment
3. For Google Colab: Copy and paste directly
===============================================================================
"""

"""
K-Means Clustering Implementation in Python
==========================================

This module provides a complete implementation of the K-Means clustering algorithm.
It includes error handling, example usage, and visualization.

Author: [Your Name]
Date: [Today's Date]
"""

import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

class KMeans:
    """
    K-Means Clustering Algorithm

    Attributes:
        k (int): Number of clusters
        max_iter (int): Maximum number of iterations
        tol (float): Tolerance for convergence
        centroids (numpy.array): Cluster centroids
        labels (numpy.array): Cluster labels for each data point
    """

    def __init__(self, k, max_iter=100, tol=1e-4):
        """
        Initialize the K-Means clustering algorithm

        Args:
            k (int): Number of clusters
            max_iter (int, optional): Maximum number of iterations. Defaults to 100.
            tol (float, optional): Tolerance for convergence. Defaults to 1e-4.
        """
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.centroids = None
        self.labels = None

    def _initialize_centroids(self, X):
        """
        Initialize cluster centroids using K-Means++ initialization

        Args:
            X (numpy.array): Input data

        Returns:
            numpy.array: Initialized cluster centroids
        """
        # Choose the first centroid randomly
        centroids = [X[np.random.choice(range(X.shape[0]))]]

        # Choose the remaining centroids using K-Means++ initialization
        for _ in range(1, self.k):
            # Calculate the squared distances from each data point to the closest centroid
            dist2 = np.array([min([np.inner(c - x, c - x) for c in centroids]) for x in X])
            # Choose the next centroid with probability proportional to the squared distance
            probs = dist2 / dist2.sum()
            cumulative_probs = probs.cumsum()
            r = np.random.rand()
            # Select the next centroid
            for j, p in enumerate(cumulative_probs):
                if r < p:
                    i = j
                    break
            centroids.append(X[i])

        return np.array(centroids)

    def _assign_labels(self, X):
        """
        Assign cluster labels to each data point

        Args:
            X (numpy.array): Input data

        Returns:
            numpy.array: Cluster labels for each data point
        """
        # Calculate the squared distances from each data point to each centroid
        dist2 = np.array([[np.inner(c - x, c - x) for c in self.centroids] for x in X])
        # Assign the label of the closest centroid to each data point
        labels = np.argmin(dist2, axis=1)
        return labels

    def _update_centroids(self, X, labels):
        """
        Update cluster centroids

        Args:
            X (numpy.array): Input data
            labels (numpy.array): Cluster labels for each data point

        Returns:
            numpy.array: Updated cluster centroids
        """
        # Update the centroids by taking the mean of all data points in each cluster
        centroids = np.array([X[labels == i].mean(axis=0) for i in range(self.k)])
        return centroids

    def fit(self, X):
        """
        Fit the K-Means clustering algorithm to the input data

        Args:
            X (numpy.array): Input data

        Returns:
            KMeans: The fitted K-Means clustering algorithm
        """
        try:
            # Initialize the centroids
            self.centroids = self._initialize_centroids(X)

            # Iterate until convergence or maximum number of iterations
            for _ in range(self.max_iter):
                # Assign labels to each data point
                prev_labels = self.labels
                self.labels = self._assign_labels(X)

                # Update the centroids
                prev_centroids = self.centroids
                self.centroids = self._update_centroids(X, self.labels)

                # Check for convergence
                if np.all(self.centroids == prev_centroids) or np.all(self.labels == prev_labels):
                    break

            return self

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def predict(self, X):
        """
        Predict the cluster labels for the input data

        Args:
            X (numpy.array): Input data

        Returns:
            numpy.array: Predicted cluster labels
        """
        try:
            # Assign labels to each data point
            labels = self._assign_labels(X)
            return labels

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Generate sample data
    X, _ = make_blobs(n_samples=200, centers=3, n_features=2, random_state=0)

    # Create a K-Means clustering algorithm with 3 clusters
    kmeans = KMeans(k=3)

    # Fit the K-Means clustering algorithm to the data
    kmeans.fit(X)

    # Predict the cluster labels
    labels = kmeans.predict(X)

    # Evaluate the clustering using the silhouette score
    score = silhouette_score(X, labels)
    print(f"Silhouette score: {score}")

    # Visualize the clustering
    plt.scatter(X[:, 0], X[:, 1], c=labels)
    plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], c='red', marker='x', s=200)
    plt.show()