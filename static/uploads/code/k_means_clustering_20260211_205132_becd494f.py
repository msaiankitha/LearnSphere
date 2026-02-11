"""
===============================================================================
ML Learning Assistant - Generated Code
Topic: k means clustering
Generated on: 2026-02-11 20:51:32

DEPENDENCIES:
pip install scikit-learn
pip install numpy
pip install matplotlib

INSTRUCTIONS:
1. Install required dependencies using pip
2. Run this script in your Python environment
3. For Google Colab: Copy and paste directly
===============================================================================
"""

"""
K-Means Clustering Implementation in Python

This script provides a complete implementation of the K-Means clustering algorithm.
It includes necessary imports, error handling, and example usage.

Author: [Your Name]
Date: [Today's Date]
"""

# Import necessary libraries
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

def kmeans_clustering(data, k):
    """
    Perform K-Means clustering on the given data.

    Args:
        data (numpy.array): Input data points
        k (int): Number of clusters

    Returns:
        labels (numpy.array): Cluster labels for each data point
        centers (numpy.array): Coordinates of the cluster centers
    """
    try:
        # Initialize the K-Means model with k clusters
        kmeans = KMeans(n_clusters=k)

        # Fit the model to the data
        kmeans.fit(data)

        # Get the cluster labels and centers
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_

        return labels, centers

    except ValueError as e:
        print(f"Error: {e}")
        return None

def visualize_clusters(data, labels, centers):
    """
    Visualize the clusters using matplotlib.

    Args:
        data (numpy.array): Input data points
        labels (numpy.array): Cluster labels for each data point
        centers (numpy.array): Coordinates of the cluster centers
    """
    try:
        # Create a scatter plot of the data points
        plt.scatter(data[:, 0], data[:, 1], c=labels)

        # Plot the cluster centers
        plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='*', s=200)

        # Show the plot
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

def main():
    # Generate sample data using make_blobs
    data, _ = make_blobs(n_samples=200, centers=3, n_features=2, random_state=1)

    # Perform K-Means clustering with k=3
    k = 3
    labels, centers = kmeans_clustering(data, k)

    # Visualize the clusters
    if labels is not None and centers is not None:
        visualize_clusters(data, labels, centers)

if __name__ == "__main__":
    main()