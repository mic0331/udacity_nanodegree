#!/usr/bin/python
from __future__ import division

import sys
from time import time
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
from enron import preparation, feature_processing, evaluation
from enron.algorithm import ClassificationPipelines
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB

import numpy as np

from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import f_classif
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from sklearn import cross_validation
import matplotlib.pyplot as plt

###########################################################################
### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
###########################################################################
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances',
                 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value',
                 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive',
                 'restricted_stock', 'director_fees', 'to_messages', 
                 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 
                 'shared_receipt_with_poi']

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### uncomment to see basic statistics of the dataset
#preparation.get_characteristics(data_dict)

###########################################################################
### Task 2: Remove outliers
###########################################################################

### uncomment to see the max NaN per record
#max_na = preparation.get_max_Nan(data_dict, features_list)
### uncomment to see the person(s) with the highest number of NaN
#preparation.get_person_highest_NaN(data_dict, features_list, max_na)

data_dict = preparation.remove_outliers(data_dict)

###########################################################################
### Task 3: Create new feature(s)
###########################################################################

data_dict, features_list = feature_processing.create_email_ratio(data_dict, features_list)

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True, remove_NaN=False)
labels, features = targetFeatureSplit(data)

# Impute all missing values with the mean of the feature
features = feature_processing.impute(features, strategy = 'mean')

# Check if we have any constance features
#print np.std(features, axis=0) == 0

### scaling features
features = feature_processing.scale(features)

###########################################################################
### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
###########################################################################

###########################################################################
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
###########################################################################

# StratifiedShuffleSplits for 1000 internal cross-validation splits
# within the grid-search.
skfold = StratifiedShuffleSplit(labels, n_iter=1000, test_size=0.1)


# find the best algorithm offering the highest recall
algorithms = ClassificationPipelines()
metric = 'recall'

best_estimator = {
    'name': '',
    'estimator' : '',
    'n_pca_components' : 0,
    'score' : 0.,
    'nbr_features_selected' : 0,
    'top_features' : [],
    'best_params': []
}

# loop over a variety of classifier to pick the best against the metric of 
# choice
for classifier_name, pipeline, params, enable in algorithms.get_models():    
    # Note : for performance reason, only the winning classifier is enable
    if enable == True: 
        print "************ Implementing {0} ************".format(classifier_name)
        # Implement the grid search by prugging the pipline and the params.
        # Optimize the grid with skfold
        # switch verbose to 0 to hide processing steps in the console
        print params
        grid_search = GridSearchCV(pipeline, param_grid=params, cv=skfold,
                               n_jobs=-1, scoring=metric, verbose=1)
        
        # fit the model in the grid search
        grid_search.fit(features, labels)

        # We sort the results, and determine the best-performing tuning parameters.
        sorted(grid_search.grid_scores_, key=lambda x: x.mean_validation_score)

        if grid_search.best_score_ > best_estimator['score']:
            best_estimator['name'] = classifier_name
            best_estimator['estimator'] = grid_search.best_estimator_
            best_estimator['n_pca_components'] = grid_search.best_estimator_.named_steps['reducer'].n_components_
            best_estimator['score'] = grid_search.best_score_
            mask = grid_search.best_estimator_.named_steps['selecter'].get_support()
            top_features = [x for (x, boolean) in zip(features_list[1:], mask) if boolean]
            best_estimator['top_features'] = top_features
            best_estimator['nbr_features_selected'] = len(top_features)
            best_estimator['best_params'] = grid_search.best_params_        

print "." * 80
print "Winning  classifier for the best {0} is {1}".format(metric, best_estimator['name'])
print "Cross-validated {0} score: {1}".format(metric, best_estimator['score'])
print "{0} features selected".format(best_estimator['nbr_features_selected'])
print "Top features : ", best_estimator['top_features']
print "Reduced to {0} PCA components".format(
    best_estimator['n_pca_components'])
print "Best parameters", best_estimator['best_params']
print "." * 80


clf = best_estimator['estimator']

test_classifier(clf, my_dataset, features_list)

### Dump your classifier, dataset, and features_list so 
### anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)