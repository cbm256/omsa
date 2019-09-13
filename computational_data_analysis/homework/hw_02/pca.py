import pandas as pd
import numpy as np
import seaborn as sns

sns.set()
import matplotlib.pyplot as plt
import requests
import scipy.sparse.linalg
import scipy as sp
import scipy.sparse


df = pd.read_csv("food-consumption.csv").dropna().reset_index(drop=True)
X = df.iloc[:, 1:].as_matrix()
m, n = X.shape

# Get data to classify countries into regions
r = requests.get("https://restcountries.eu/rest/v2/region/europe")
countries = r.json()

regions = {c: {} for c in df["Country"]}

for c in countries:
    if c["name"] in regions.keys():
        regions[c["name"]] = c["subregion"]


regions["Holland"] = "Western Europe"
regions["England"] = "Northern Europe"
regions = [v for k, v in regions.items()]

# PCA using eigendecomposition
# step 1: estimate the mean and covariance matrix
mu = np.mean(X, axis=0).reshape(1, 20)
X_scaled = np.subtract(X, mu)
C = np.dot(X_scaled.T, X_scaled) / m
# step 2: perform eigendecomposition on the covariance matrix
w, v = np.linalg.eig(C)
# Order the data
idx = w.argsort()[::-1]
principal_directions = v[:, idx]
# step 3: Compute reduced Representation
principal_components_ed = np.dot(
    X_scaled / np.sqrt(w[idx].reshape(1, 20)), principal_directions.T
)
# Plot the first 2 principal directions
ax = sns.scatterplot(x=principal_directions[:, 0], y=principal_directions[:, 1])
# Plot the first two principal components
ax = sns.scatterplot(
    x=principal_components_ed[:, 0], y=principal_components_ed[:, 1], hue=regions
)


# PCA using SVD
U, S, V = np.linalg.svd(X_scaled, full_matrices=False, compute_uv=True)

principal_components_svd = np.dot(U, np.diag(S))
ax = sns.scatterplot(
    x=principal_components_svd[:, 0], y=principal_components_svd[:, 1], hue=regions
)


# PCA using scipy linalg

# step 1: estimate the mean and covariance matrix
mu = np.mean(X, axis=0).reshape(1, 20)
X_scaled = np.subtract(X, mu)
C = np.dot(X_scaled.T, X_scaled) / m
# step 2: perform eigendecomposition on the covariance matrix
w, v = np.linalg.eig(C)
w, v = sp.sparse.linalg.eigs(C, k=n, which="LR")
# step 3: Compute reduced Representation
principal_components_sp = np.dot(X_scaled / np.sqrt(w.reshape(1, 20)), v.T)

ax = sns.scatterplot(
    x=principal_components_sp[:, 0], y=principal_components_sp[:, 1], hue=regions
)


# PCA using Sklearn
pca = PCA()
principal_components_sk = pca.fit_transform(X_scaled)
ax = sns.scatterplot(
    x=principal_components_sk[:, 0], y=principal_components_sk[:, 1], hue=regions
)

