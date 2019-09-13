import pandas as pd
import scipy as sp
import scipy.sparse
import scipy.sparse.linalg
from sklearn.metrics import confusion_matrix
import numpy as np

from homework.hw_02.my_sol_kmeans import my_kmeans

df = pd.read_csv("edges.txt", sep="\t", header=None, names=["org", "dest"])
nodes = pd.read_csv("nodes.txt", sep="\t", header=None, names=["blog", "class", "site"])
df["weight"] = 1
df["org"] = df["org"] - 1
df["dest"] = df["dest"] - 1

# Step 1: represent graph as adjacency matrix
A = sp.sparse.coo_matrix((df["weight"], (df["org"], df["dest"])), shape=(1490, 1490))
# Step 2: form a special matrix L=D-A, the graph Laplacian
D = sp.sparse.diags(np.array(np.sum(A, axis=0))[0])
L = D - A
fcr = []
for i in range(20):
    # Step 3: compute k eigenvectors, v1,v2...vk corresponding to the k smallest eigenvalues (k ≪ m)
    w, Z = sp.sparse.linalg.eigs(L, k=2, which="SR")
    # Step 4: run kmeans algorithm on Z = (v1,v2,...vk) by treating each row as a new data point
    classes, centroids = my_kmeans(Z, 2)

    # Find the false classification rate
    y_true = [int(float(x)) for x in nodes["class"]]
    y_pred = classes
    y_pred2 = [1 if x == 0 else 0 for x in classes]
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    cm = pd.DataFrame({"Predicted No": [tn, fn], "Predicted Yes": [fp, tp]})
    cm.index = ["Actual No", "Actual Yes"]
    false_classification_rate = (fp + fn) / 1490 * 100
    fcr.append(np.round(false_classification_rate))

np.sum(fcr) / len(fcr)
