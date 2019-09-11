import numpy as np


def get_distances(centroids, pixels, ord=None):
    distances = []
    for centroid in centroids:
        distances.append(np.linalg.norm((centroid - pixels), axis=1, ord=ord))
    return distances


def join_distances(distances):
    distances = [x.reshape((x.shape[0], 1)) for x in distances]
    distances_joined = np.concatenate(distances, axis=1)
    return distances_joined


def get_min_distance(distances_joined):
    min_distances = np.min(distances_joined, axis=1)
    return min_distances


def get_probabilities(min_distances):
    dis_sq = np.square(min_distances)
    a = np.sum(dis_sq)
    p = np.multiply(1 / a, dis_sq)

    return p


def get_centroid(centroids, pixels, ord=None):
    distances = get_distances(centroids, pixels, ord=ord)
    distances_joined = join_distances(distances)
    min_distances = get_min_distance(distances_joined)
    p = get_probabilities(min_distances)
    idxs = [x for x in range(pixels.shape[0])]
    idx = np.random.choice(idxs, 1, p=p)
    return pixels[idx]


def k_plus_plus(pixels, K):
    pixels_copy = pixels.copy()
    np.random.shuffle(pixels_copy)

    centroids = pixels_copy[0, :].reshape(1, pixels_copy.shape[1])

    while len(centroids) < K:
        new_centroid = get_centroid(centroids, pixels).reshape(1, pixels_copy.shape[1])
        centroids = np.append(centroids, new_centroid, axis=0)

    return centroids


def get_classes(centroids, pixels, ord=None):
    distances = get_distances(centroids, pixels, ord=ord)
    distances_joined = join_distances(distances)
    classes = np.argmin(distances_joined, axis=1)
    return classes


def get_new_centroids(centroids, pixels):
    classes = get_classes(centroids, pixels)
    new_centroids = np.zeros(shape=centroids.shape)
    for i in range(len(centroids)):
        centroid = np.mean(pixels[classes == i], axis=0)
        new_centroids[i] = centroid

    return new_centroids


def get_centroids(pixels, K, ord=None):
    centroids = k_plus_plus(pixels, K)
    c = np.full(centroids.shape, np.inf)
    centroid_distances = np.linalg.norm((centroids - c), axis=0, ord=ord)
    while np.max(centroid_distances) > 1:
        new_centroids = get_new_centroids(centroids, pixels)
        centroid_distances = np.linalg.norm(
            (centroids - new_centroids), axis=1, ord=ord
        )
        centroids = new_centroids
    return centroids


def my_kmeans(pixels, K, ord=None):
    centroids = get_centroids(pixels, K, ord=ord)
    classes = get_classes(centroids, pixels, ord=ord)
    return classes, centroids
