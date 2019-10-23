from sklearn.metrics import mean_squared_error
import numpy as np

X = np.array([[4, -2, 4], [5, -3,5], [2,0,2], [3,-1,3]]).reshape(4,3)
m,n=X.shape
X_centered = (X - np.mean(X, axis = 0)) / np.std(X, axis=0)
cov = np.dot(X_centered.T,X_centered)/(X_centered.shape[0]-1)
eig_val,eig_vec=np.linalg.eig(cov)
pcs = eig_vec[:,eig_val.argsort()[::-1]]
feature_vector = pcs[:,:1]
final_data = np.dot(feature_vector.T, X_centered.T).T
reconstructed = np.dot(feature_vector, final_data.T).T + np.mean(X, axis = 0).reshape(1,n) * np.std(X, axis=0)

# first principal direction
print(pcs[:,0])
# Reconstruction error
print(pcs[:,1:].sum())