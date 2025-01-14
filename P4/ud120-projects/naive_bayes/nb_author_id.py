#!/usr/bin/python

""" 
    this is the code to accompany the Lesson 1 (Naive Bayes) mini-project 

    use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
    Sara has label 0
    Chris has label 1

"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn.naive_bayes import GaussianNB


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

### create classifier
clf = GaussianNB()
### fit the classifier on the training features and labels
t0 = time()
clf.fit(features_train,labels_train)
print 'training time',round(time()-t0,3) ,'s'
### use the trained classifier to predict labels for the test features
t0 = time()
pred = clf.predict(features_test)
print 'predicting time', round(time()-t0,3),'s'
### calculate the accuracy on the test data
print 'Accuracy', clf.score(features_test, labels_test)


#########################################################


