import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
import networkx as nx


def Matrix_D(W):
    # Generate Graph and Obtain Matrix D, \\
    # from weight matrix W defining the weight on the edge between each pair of nodes.
    # Note that you can assign sufficiently large weights to non-existing edges.
    
    # Package networkx (version 1.11) is required

    n = np.shape(W)[0]
    Graph = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            Graph.add_weighted_edges_from([(i,j,min(W[i,j], W[j,i]))])

    res = nx.all_pairs_dijkstra_path_length(Graph)
    D = np.zeros([n,n])
    for i in range(n):
        for j in range(n):
            D[i,j] = res[i][j]
    np.savetxt('D.csv', D)
    return D

imgs = pd.read_csv('isomap.csv', header=None)
imgs.shape

X = imgs.values.T

dists = cdist(X, X, 'euclidean')
def get_a_matrix(a):
    idx = a.argsort().argsort()
    idx = np.array([1 if x <=100 and x>0 else 0 for x in idx]).reshape(idx.shape)
    return idx
def get_w_matrix(a):
    idx = a.argsort().argsort()
    idx = np.array([x if x <= 100 else 110 for x in idx]).reshape(idx.shape)
    return idx

A = np.apply_along_axis(get_a_matrix, 1, dists)
W = np.apply_along_axis(get_w_matrix, 1, dists)


fig, ax = plt.subplots(figsize=(10,10))
ax = sns.heatmap(W,cmap="YlGnBu")

D = Matrix_D(W)

m,_ = D.shape
I = np.identity(m)
ones = np.ones(D.shape)
H = I - (ones * 1/m)
C = np.dot(np.dot(H,D*D),H) * -1/(2*-10000000)
vals, vecs = np.linalg.eig(C)
pc_vals = vals[vals.argsort()[::-1]]
pcs = vecs[vals.argsort()[::-1]]

Zt = np.dot(pcs[:,:2],np.diag(pc_vals[:2]**(-.5)))
d = pd.DataFrame(Zt)

#embedding plot
d.plot.scatter(x=0,y=1)

# faces plot
Zt_dists = cdist(Zt, Zt, 'euclidean')
W_Zt = np.apply_along_axis(get_w_matrix, 1, Zt_dists)

row = 2
start = 5
end = start + 3

close = W_Zt[start].argsort().argsort()[start:end]



image_list = []
start = 5
end = start + 5
for i in range(X.shape[0]):
    row = []
    closest = W_Zt[i].argsort().argsort()[start:end]
    for j in range(len(closest)):
        row.append(X[closest[j],:].reshape(64,64))
    image_list.append(row)


s,e = (57,60)

f, axarr = plt.subplots(e-s,5)
for i,val in enumerate(image_list[s:e]):
    for j,v in enumerate(val):
        axarr[i,j].imshow(v)
        