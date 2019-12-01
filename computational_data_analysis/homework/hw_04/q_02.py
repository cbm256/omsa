import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# Part a
RANDOM_STATE = 42


def get_accuracy(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    gnb = GaussianNB()
    clf = LogisticRegression(random_state=RANDOM_STATE, solver="liblinear")
    knn = KNeighborsClassifier(n_neighbors=5)

    models = {"Naive Bayes": gnb, "Logistic Regression": clf, "KNN": knn}
    acc = {}
    for k, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        acc[k] = accuracy
    return acc


# Part b
def plots(X, y):
    gnb = GaussianNB()
    clf = LogisticRegression(random_state=RANDOM_STATE, solver="liblinear")
    knn = KNeighborsClassifier(n_neighbors=5)

    models = {"Naive Bayes": gnb, "Logistic Regression": clf, "KNN": knn}
    fitted = {k: v.fit(X[:, :2], y) for k, v in models.items()}

    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    i = 0
    for k, v in fitted.items():

        plt.subplot(2, 2, i + 1)
        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        Z = v.predict(np.c_[xx.ravel(), yy.ravel()])

        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, alpha=0.8)

        colors = ["green", "white"]
        label = ["No Divorce", "Divorce"]
        for i, c in enumerate(colors):
            plt.scatter(X[:, 0][y == i], X[:, 1][y == i], c=c, label=label[i])
        plt.legend(bbox_to_anchor=(1, 0.5))
        plt.xlabel("Feauture 1")
        plt.ylabel("Feature 2")
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.xticks(())
        plt.yticks(())
        plt.title(k)

        plt.show()
        i += 1


# Part 1a
data = pd.read_csv("q3.csv", header=None)
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

get_accuracy(X, y)

# Part 1b
plots(X, y)

# Part 2a

X = pd.read_csv("data.dat", sep="   ", header=None).to_numpy().T
y = pd.read_csv("label.dat", sep="   ", header=None)
y = y.applymap(lambda x: int(1) if x > 2 else int(0)).to_numpy().reshape(y.shape[1])


get_accuracy(X, y)

