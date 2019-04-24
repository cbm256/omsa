## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('Q3/eeg_dataset.csv')
data.head()
# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size = .3, random_state = random_state, shuffle = True)

# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
modelLr = LinearRegression()
modelLr.fit(x_train, y_train)


# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.
# XXX
y_pred_train = [int(round(x)) for x in modelLr.predict(x_train)]
accuracy_score(y_train, y_pred_train)


y_pred_test = [int(round(x)) for x in modelLr.predict(x_test)]
accuracy_score(y_test, y_pred_test)

# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX

modelRf = RandomForestClassifier()
modelRf.fit(x_train, y_train)


# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
y_pred_train = modelRf.predict(x_train)
accuracy_score(y_train, y_pred_train)

y_pred_test = [int(round(x)) for x in modelRf.predict(x_test)]
accuracy_score(y_test, y_pred_test)

# XXX
# TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
# XXX

## reference: https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
importances = modelRf.feature_importances_
std = np.std([tree.feature_importances_ for tree in modelRf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]
print("Feature ranking:")

for f in range(x_train.shape[1]):
    print("%d. feature X%d (%f)" % (f + 1, indices[f], importances[indices[f]]))


# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
n_estimators = [1, 100, 1000]
max_depth = [1, 100, 200]
parameters = {'n_estimators':n_estimators, 'max_depth':max_depth}

clfRf = GridSearchCV(RandomForestClassifier(), parameters, cv=10)
clfRf.fit(x_train, y_train)
clfRf.best_params_
clfRf.best_score_
# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# TODO: Create a SVC classifier and train it.
# XXX
scaler = StandardScaler()
scaler.fit(x_train)
x_train_scaled = scaler.transform(x_train)
x_test_scaled = scaler.transform(x_test)

modelSvc = SVC()
modelSvc.fit(x_train_scaled, y_train)


# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
y_pred_train = modelSvc.predict(x_train_scaled)
accuracy_score(y_train, y_pred_train)

y_pred_test = modelSvc.predict(x_test_scaled)
accuracy_score(y_test, y_pred_test)

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
C = [.01, 100, 1000]
kernel = ['rbf', 'linear']

parameters = {'C':C, 'kernel':kernel}

clf = GridSearchCV(SVC(), parameters, cv=10, n_jobs=-1)
clf.fit(x_train_scaled, y_train)
clf.best_params_
clf.best_score_
clf.cv_results_
# ######################################### Principal Component Analysis #################################################
# XXX
# TODO: Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# XXX

pca = PCA(n_components=10, svd_solver="full")
pca.fit(x_train)
pca.explained_variance_ratio_
pca.singular_values_
