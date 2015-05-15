#!/usr/bin/python

""" 
    this is the code to accompany the Lesson 2 (SVM) mini-project

    use an SVM to identify emails from the Enron corpus by their authors
    
    Sara has label 0
    Chris has label 1

"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
#One way to speed up an algorithm is to train it on a smaller training dataset. 
#The tradeoff is that the accuracy almost always goes down when you do this

#features_train = features_train[:len(features_train)/100] 
#labels_train = labels_train[:len(labels_train)/100] 

# Only 1% of the features, but over 88% the performance? Not too shabby!
### your code goes here ###
from sklearn.svm import SVC
clf = SVC(kernel='rbf', C=10000.)
# C = 10 ==>    0.616040955631
# C = 100 ==>   0.616040955631
# C = 1000 ==>  0.821387940842
# C = 10000 ==> 0.892491467577
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
print '10 :: ', pred[10]
print '10 :: ', pred[26]
print '10 :: ', pred[50]
print 'Size of pred', len(pred)
n = []
[n.append(e) for e in pred if e == 1]
print 'Chris ', len(n)
#########################################################