from util import entropy, information_gain, partition_classes
import numpy as np
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        self.tree = {}


    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree

        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        def determine_terminal(x,y):

            if len(set(y)) == 1 or len(np.unique(x)) == 1:
                return True
            else:
                return False

        def get_best_feature(X,y):
            #reference: https://stackoverflow.com/a/6473724/4296857


            best_info_gain = np.float("-inf")
            previous_y = [y]

            for split_attribute, col in enumerate(X.T):
                for split_val in np.unique(col):

                    X_left, X_right, y_left, y_right = list(partition_classes(X, y, split_attribute, split_val))
                    current_y = [y_left, y_right]
                    ig = information_gain(previous_y, current_y)
                    if ig>best_info_gain:
                        previous_y = current_y
                        best_info_gain = ig
                        best_split_attribute = split_attribute
                        best_split_val = split_val
                        best_X_left, best_X_right, best_y_left, best_y_right = X_left, X_right,  y_left, y_right

            return [best_info_gain, best_split_attribute, best_split_val, best_X_left, best_X_right, best_y_left, best_y_right]

        X = np.array([np.array(l, dtype = object) for l in X])
        y = np.array([np.array(l) for l in y])

        result = {'x':X,'y':y}

        leaf_list = [result]

        while leaf_list:
            leaf = leaf_list.pop(0)
            x = leaf['x']
            y = leaf['y']
            if determine_terminal(x,y):
                predict = max(y, key = lambda x: len([i for i in list(set(y)) if i == x]))
                leaf.update({"predict":predict})
                leaf.pop("x")
                leaf.pop("y")
                continue
            else:
                feature = get_best_feature(x,y)
                best_info_gain, best_split_attribute, best_split_val, best_X_left, best_X_right, best_y_left, best_y_right = feature
                left_leaf = {"x":best_X_left, "y":best_y_left}
                right_leaf = {"x":best_X_right, "y":best_y_right}
                leaf.update({"split_attribute":best_split_attribute, "split_val":best_split_val,"left":left_leaf, "right":right_leaf})
                leaf.pop("x")
                leaf.pop("y")
                leaf_list.append(left_leaf)
                leaf_list.append(right_leaf)


        self.tree.update(result)
        return result



    def classify(self, record):

        def classifyRecord(record,resultDict):
            if "predict" in list(resultDict.keys()):
                return resultDict["predict"]
            else:
                split_attribute = resultDict["split_attribute"]
                split_val = resultDict["split_val"]
                X_left, X_right, _, _= list(partition_classes(record, [[]], split_attribute, split_val))
                if X_left.any():
                    resultDict = resultDict["left"]
                    record = X_left
                else:
                    resultDict = resultDict["right"]
                    record = X_right
                return classifyRecord(record,resultDict)

        return classifyRecord([record],self.tree)
