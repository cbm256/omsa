from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.samples.definitions import FCPS_SAMPLES
from pyclustering.utils import read_sample
from pyclustering.utils.metric import distance_metric
from pyclustering.utils.metric import type_metric
import numpy as np
from sklearn.cluster import KMeans


X = np.array([[2, 2], [-1, 1], [3, 1],
               [0, -1], [-2, -2]])
initial_centers = np.array([[-3, -1], [2, 1]])

#Euclidean
kmeans = KMeans(n_clusters=2, init=initial_centers, max_iter = 1).fit(X)
print(kmeans.labels_)
print(kmeans.cluster_centers_)


kmeans = KMeans(n_clusters=2, init=initial_centers, max_iter = 50).fit(X)
print(kmeans.labels_)
print(kmeans.cluster_centers_)

#Manhattan

X = np.array([[2, 2], [-1, 1], [3, 1],[0, -1], [-2, -2]])

initial_centers = np.array([[-3, -1], [2, 1]])

manhattan_metric = distance_metric(type_metric.MANHATTAN)

kmeans_instance = kmeans(X, initial_centers, 1, metric=manhattan_metric)
kmeans_instance.process()
clusters = kmeans_instance.get_clusters()
final_centers = kmeans_instance.get_centers()

kmeans_instance_50 = kmeans(X, initial_centers, 50, metric=manhattan_metric)
kmeans_instance_50.process()
clusters_50 = kmeans_instance_50.get_clusters()
final_centers_50 = kmeans_instance_50.get_centers()


print(clusters)
print(final_centers_50)