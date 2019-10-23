from sklearn.cluster import SpectralClustering
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[-1, 2], [-1, 1], [-1, 0],
               [-1, -1], [-1, -2], [0, 0],[1, 0],[2, 0]])
clustering = SpectralClustering(n_clusters=2,
         assign_labels="kmeans",
         random_state=0, affinity='nearest_neighbors', n_neighbors=2).fit(X)
print(clustering.labels_ )


kmeans = KMeans(n_clusters=2, max_iter = 100).fit(X)
print(kmeans.labels_)