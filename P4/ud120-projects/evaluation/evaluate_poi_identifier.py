# coding: utf-8
#!/usr/bin/python


"""
    starter code for the evaluation mini-project
    start by copying your trained/tested POI identifier from
    that you built in the validation mini-project

    the second step toward building your POI identifier!

    start by loading/formatting the data

"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
import numpy as np
from sklearn import metrics

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)


features_train,features_test,labels_train,labels_test = cross_validation.train_test_split(features,labels,test_size=0.3,
                                                                                           random_state=42)
clf = DecisionTreeClassifier()
clf.fit(features_train,labels_train)
print "Score / deploying training-testing regime", clf.score(features_test,labels_test)


predict_on_test = clf.predict(features_test)
print np.array(predict_on_test)
print "How many POIs are in the test set for your POI identifier?", len([e for e in predict_on_test if e == 1.0])
print "How many people totat are in your test set?", len(features_test)
print "If your identifier predicted 0. (not POI) for everyone in the test set, what would its accuracy be?", (29.-3.)/29.
print "What’s the precision?", metrics.precision_score(labels_test, predict_on_test)
print "What's the recall of your POI identifier?", metrics.recall_score(labels_test, predict_on_test)

predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]

print "how many true positives ?", sum(np.logical_and(predictions, true_labels))
print "how many true negatives ?", sum(np.logical_not(np.logical_or(predictions, true_labels)))
print "How many false positives are there?", sum([int(p &~ l) for p, l in zip(predictions, true_labels)])
print "How many false positives are there?", sum([int(~p & l) for p, l in zip(predictions, true_labels)])
print "What's the precision of this classifier?", metrics.precision_score(true_labels, predictions)
print "What's the recall of this classifier?", metrics.recall_score(true_labels, predictions)



