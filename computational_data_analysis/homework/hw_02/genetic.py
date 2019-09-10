#% Your goal of this assignment is implementing your own K-medoids.
#% Please refer to the instructions carefully, and we encourage you to
#% consult with other resources about this algorithm on the web.
#%
#% Input:
#%     pixels: data set. Each row contains one data point. For image
#%     dataset, it contains 3 columns, each column corresponding to Red,
#%     Green, and Blue component.
#%
#%     K: the number of desired clusters. Too high value of K may result in
#%     empty cluster error. Then, you need to reduce it.
#%
#% Output:
#%     class: the class assignment of each data point in pixels. The
#%     assignment should be 1, 2, 3, etc. For K = 5, for example, each cell
#%     of class should be either 1, 2, 3, 4, or 5. The output should be a
#%     column vector with size(pixels, 1) elements.
#%
#%     centroid: the location of K centroids in your result. With images,
#%     each centroid corresponds to the representative color of each
#%     cluster. The output should be a matrix with K rows and
#%     3 columns. The range of values should be [0, 255].
#%
#%
#% You may run the following line, then you can see what should be done.
#% For submission, you need to code your own implementation without using
#% the kmeans matlab function directly. That is, you need to comment it out.

import numpy as np
from my_sol_kmeans import k_plus_plus


def get_initial_idxs(pixels, K):
    idxs = np.array([x for x in range(pixels.shape[0])])
    np.random.shuffle(idxs)
    return idxs[:K]


def get_distances(centroids, pixels, ord=None):
    distances = []
    for centroid in centroids:
        distances.append(np.linalg.norm((centroid - pixels), axis=1, ord=ord))
    return distances


def get_closest_idxs(distances):
    idxs = np.array(distances).argsort()
    closest_idxs = idxs[:, 0]
    return closest_idxs


def join_distances(distances):
    distances = [x.reshape((x.shape[0], 1)) for x in distances]
    distances_joined = np.concatenate(distances, axis=1)
    return distances_joined


def get_classes(centroids, pixels, ord=None):
    distances = get_distances(centroids, pixels, ord=ord)
    distances_joined = join_distances(distances)
    classes = np.argmin(distances_joined, axis=1)
    return classes


def get_cost(centroids, pixels, classes, ord=None):

    cost = 0
    for i, v in enumerate(centroids):
        centroid = v
        pxls = pixels[classes == i]
        d = np.linalg.norm((centroid - pxls), axis=1, ord=ord)
        cost += np.sum(d)
    return cost


def mutate(pixels, centroid):
    idxs = np.array([x for x in range(pixels.shape[0])])
    np.random.shuffle(idxs)
    rand_idx = np.random.randint(0, centroid.shape[0])
    new_centroids = centroid.copy()
    new_centroids[rand_idx] = idxs[0]
    return new_centroids


def crossover(centroid_list):
    K = centroid_list[0].shape[0]
    all_centroids = np.concatenate(centroid_list)
    np.random.shuffle(all_centroids)
    new_centroid_list = []
    old_range = 0
    for i in range(0, K + 1):
        new_range = (i + 1) * K
        centroids = all_centroids[old_range:new_range]
        new_centroid_list.append(centroids)
        old_range = new_range
    return new_centroid_list


def get_best_centroids(centroid_list, pixels, class_list):
    class_list = [get_classes(centroids, pixels) for centroids in centroid_list]
    # Calculate the initial total cost which is the sum of all distances.
    costs = np.array(
        [
            get_cost(centroids, pixels, classes)
            for centroids, classes in zip(centroid_list, class_list)
        ]
    )
    idxs = costs.argsort()
    centroids = np.array(centroid_list)[idxs[:11]]
    centroid_list = [centroids[i] for i in range(centroids.shape[0])]
    return centroid_list


def my_kmedoids(pixels, K, initial_centroids=False, RUNS=200, ord=None):
    # initialize k cluster centers by randomly choosing k points from within x^n
    if not initial_centroids:
        centroid_list = []
        for i in range(20):

            idxs = list(get_initial_idxs(pixels, K))
            idxs.sort()
            centroids = pixels[idxs].reshape(K, 3)
            centroid_list.append(centroids)

    else:
        assert initial_centroids.shape[0] == K
        centroids = initial_centroids

    class_list = [get_classes(centroids, pixels) for centroids in centroid_list]
    centroid_list = get_best_centroids(centroid_list, pixels, class_list)

    runs = 0
    while runs < RUNS:

        cross_overs = crossover(centroid_list)
        mutates = [mutate(pixels, centroid) for centroid in centroid_list]
        centroid_list = centroid_list + cross_overs + mutates
        class_list = [get_classes(centroids, pixels) for centroids in centroid_list]
        centroid_list = get_best_centroids(centroid_list, pixels, class_list)
        runs += 1
    # Generate classes from best set of cluster centers
    centroids = centroid_list[0]
    classes = get_classes(centroids, pixels)

    return classes, centroids

