# -*- coding: utf-8 -*-
#!/usr/bin/python

from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import f_classif
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

class ClassificationPipelines:
    """
        class used to abstract the papline and parameters used in the
        GridSearchCV algorithm.
        This class mainly return an array of models.
        A model contain contain :
            * a boolean indicating if the model is active or 
            not during the processing of the GridSearchCV
            * a Pipeline object containing the steps involved in the 
            GridSearchCV
            * the parameters of the pipeline for each steps
            * the name of the model
        The selected parameters are those showing the best results for the 
        model, feel free to uncomment the trailing comments next to each 
        parameters to see how the grid is selecting the most appropriate 
        combination

    """
    def __init__(self):
        # The scoring function used is NOVA F-value between labe/feature for 
        # classification tasks.
        self.score_func = f_classif   
        # Note : Any parameters not grid searched over are determined by this estimator 
        self.models = [
            (
                "Logistic Regression Model",
                Pipeline(steps=[
                    ('selecter', SelectKBest(score_func=self.score_func)),
                    ('reducer', PCA()),
                    ('classifier', LogisticRegression())
                    ]),
                {
                    # Number of top features to select. The “all” option 
                    # bypasses selection, for use in a parameter search.
                    'selecter__k': [x for x in range (5, 20)],
                    # Number of components to keep.
                    # if 0 < n_components < 1
                    # select the number of components such that the amount of 
                    # variance that needs to be explained is greater than the 
                    # percentage specified by n_components
                    'reducer__n_components': [5], 
                    # When True (False by default) the components_ vectors are 
                    # divided by n_samples times singular values to ensure 
                    # uncorrelated outputs with unit component-wise variances.
                    # Whitening will remove some information from the 
                    # transformed signal (the relative variance scales of the # components) but can sometime improve the predictive # 
                    # accuracy of the downstream estimators by making there 
                    # data respect some hard-wired assumptions.
                    'reducer__whiten': [False],
                    # Over-/undersamples the samples of each class according 
                    # to the given weights. If not given, all classes are 
                    # supposed to have weight one. The ‘auto’ mode selects 
                    # weights inversely proportional to class frequencies in 
                    # the training set.
                    'classifier__class_weight': ['auto'], 
                    # Tolerance for stopping criteria. 
                    'classifier__tol': [10.** x for x in np.arange(-5, -1)],
                    # Inverse of regularization strength; must be a positive 
                    # float. Like in support vector machines, smaller values 
                    # specify stronger regularization.
                    'classifier__C': [10.** x for x in np.arange(-5, -1)],
                },
                False # Enable the classifier
            ),
            (
                "Linear Support Vector Machines Classifier Model",
                Pipeline(steps=[
                    ('selecter', SelectKBest(score_func=self.score_func)),
                    ('reducer', PCA()),
                    ('classifier', LinearSVC())
                    ]),
                {
                    # Number of top features to select. The “all” option 
                    # bypasses selection, for use in a parameter search.
                    'selecter__k': [x for x in range (5, 20)],
                    # Number of components to keep.
                    # if 0 < n_components < 1
                    # select the number of components such that the amount of 
                    # variance that needs to be explained is greater than the 
                    # percentage specified by n_components
                    'reducer__n_components': [5], 
                    # When True (False by default) the components_ vectors are 
                    # divided by n_samples times singular values to ensure 
                    # uncorrelated outputs with unit component-wise variances.
                    # Whitening will remove some information from the 
                    # transformed signal (the relative variance scales of the # components) but can sometime improve the predictive # 
                    # accuracy of the downstream estimators by making there 
                    # data respect some hard-wired assumptions.
                    'reducer__whiten': [True],
                    # Set the parameter C of class i to class_weight[i]*C for 
                    # SVC. If not given, all classes are supposed to have 
                    # weight one. The ‘auto’ mode uses the values of y to 
                    # automatically adjust weights inversely proportional to 
                    # class frequencies.
                    'classifier__class_weight': ['auto'],
                    # Tolerance for stopping criteria.
                    'classifier__tol': [10.** x for x in np.arange(-5, -1)],
                    # Penalty parameter C of the error term.
                    'classifier__C': [10.** x for x in np.arange(-5, -1)]
                },
                False # Enable the classifier
            ),
            (
                "Support Vector Machines Classifier Model",
                Pipeline(steps=[
                    ('selecter', SelectKBest(score_func=self.score_func)),
                    ('reducer', PCA()),
                    ('classifier', SVC())
                    ]),
                {
                    # Number of top features to select. The “all” option 
                    # bypasses selection, for use in a parameter search.
                    'selecter__k': [12],#[x for x in range (5, 20)],
                    # Number of components to keep.
                    # if 0 < n_components < 1
                    # select the number of components such that the amount of 
                    # variance that needs to be explained is greater than the 
                    # percentage specified by n_components
                    'reducer__n_components': [5], 
                    # When True (False by default) the components_ vectors are 
                    # divided by n_samples times singular values to ensure 
                    # uncorrelated outputs with unit component-wise variances.
                    # Whitening will remove some information from the 
                    # transformed signal (the relative variance scales of the # components) but can sometime improve the predictive # 
                    # accuracy of the downstream estimators by making there 
                    # data respect some hard-wired assumptions.
                    'reducer__whiten': [True],      
                    # Penalty parameter C of the error term.              
                    'classifier__C': [1.],
                    # Specifies the kernel type to be used in the algorithm. 
                    # It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, 
                    # ‘precomputed’ or a callable. If none is given, ‘rbf’ 
                    # will be used. If a callable is given it is used to 
                    # precompute the kernel matrix.
                    'classifier__kernel': ['rbf'],
                    # Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’. If 
                    # gamma is 0.0 then 1/n_features will be used instead.
                    'classifier__gamma': [0.0],
                    # Tolerance for stopping criterion.
                    'classifier__tol': [.001],#[10.** x for x in np.arange(-5, -1)],
                    # Set the parameter C of class i to class_weight[i]*C for 
                    # SVC. If not given, all classes are supposed to have 
                    # weight one. The ‘auto’ mode uses the values of y to 
                    # automatically adjust weights inversely proportional to 
                    # class frequencies.
                    'classifier__class_weight': ['auto'],                    
                },
                True # Enable the classifier
            ),
            (
                "k-nearest Neighbors Vote Classifier Model",
                Pipeline(steps=[
                    ('selecter', SelectKBest(score_func=self.score_func)),
                    ('reducer', PCA()),
                    ('classifier', KNeighborsClassifier())
                    ]),
                {
                    # Number of top features to select. The “all” option 
                    # bypasses selection, for use in a parameter 
                    # search.             
                    'selecter__k': [x for x in range (5, 20)],
                    # Number of components to keep.
                    # if 0 < n_components < 1
                    # select the number of components such that the amount of 
                    # variance that needs to be explained is greater than the 
                    # percentage specified by n_components
                    'reducer__n_components': [5], 
                    # When True (False by default) the components_ vectors are 
                    # divided by n_samples times singular values to ensure 
                    # uncorrelated outputs with unit component-wise variances.
                    # Whitening will remove some information from the 
                    # transformed signal (the relative variance scales of the # components) but can sometime improve the predictive # 
                    # accuracy of the downstream estimators by making there 
                    # data respect some hard-wired assumptions.
                    'reducer__whiten': [True],
                    # Number of neighbors to use by default for k_neighbors 
                    # queries.
                    'classifier__n_neighbors': [x for x in range (3, 15)],     
                },
                False # Enable the classifier
            ),
            (
                "Random Forest Classifier Model",
                Pipeline(steps=[
                    ('selecter', SelectKBest(score_func=self.score_func)),
                    ('reducer', PCA()),
                    ('classifier', RandomForestClassifier())
                    ]),
                {
                    # Number of top features to select. The “all” option 
                    # bypasses selection, for use in a parameter 
                    # search.             
                    'selecter__k': [x for x in range (5, 20)],
                    # Number of components to keep.
                    # if 0 < n_components < 1
                    # select the number of components such that the amount of 
                    # variance that needs to be explained is greater than the 
                    # percentage specified by n_components
                    'reducer__n_components': [5], 
                    # When True (False by default) the components_ vectors are 
                    # divided by n_samples times singular values to ensure 
                    # uncorrelated outputs with unit component-wise variances.
                    # Whitening will remove some information from the 
                    # transformed signal (the relative variance scales of the # components) but can sometime improve the predictive # 
                    # accuracy of the downstream estimators by making there 
                    # data respect some hard-wired assumptions.
                    'reducer__whiten': [True],    
                    # Whether bootstrap samples are used when building trees.
                    'classifier__bootstrap': [True],
                    # The function to measure the quality of a split. 
                    # Supported criteria are “gini” for the Gini impurity and 
                    # “entropy” for the information gain. Note: this parameter 
                    # is tree-specific.
                    'classifier__criterion': ['gini', 'entropy']
                },
                False # Enable the classifier
            ),
            (
                "AdaBoost Classifier Model",
                Pipeline(steps=[
                    ('selecter', SelectKBest(score_func=self.score_func)),
                    ('reducer', PCA()),
                    ('classifier', AdaBoostClassifier())
                    ]),
                {
                    # Number of top features to select. The “all” option 
                    # bypasses selection, for use in a parameter 
                    # search.             
                    'selecter__k': [x for x in range (5, 20)],
                    # Number of components to keep.
                    # if 0 < n_components < 1
                    # select the number of components such that the amount of 
                    # variance that needs to be explained is greater than the 
                    # percentage specified by n_components
                    'reducer__n_components': [5], 
                    # When True (False by default) the components_ vectors are 
                    # divided by n_samples times singular values to ensure 
                    # uncorrelated outputs with unit component-wise variances.
                    # Whitening will remove some information from the 
                    # transformed signal (the relative variance scales of the # components) but can sometime improve the predictive # 
                    # accuracy of the downstream estimators by making there 
                    # data respect some hard-wired assumptions.
                    'reducer__whiten': [True],                    
                },
                False # Enable the classifier
            ),
            (
                "Naive Bayes Classifier Model",
                Pipeline(steps=[
                    ('selecter', SelectKBest(score_func=self.score_func)),
                    ('reducer', PCA()),
                    ('classifier', GaussianNB())
                    ]),
                {
                    # Number of top features to select. The “all” option 
                    # bypasses selection, for use in a parameter 
                    # search.             
                    'selecter__k': [x for x in range (5, 20)],
                    # Number of components to keep.
                    # if 0 < n_components < 1
                    # select the number of components such that the amount of 
                    # variance that needs to be explained is greater than the 
                    # percentage specified by n_components
                    'reducer__n_components': [5], 
                    # When True (False by default) the components_ vectors are 
                    # divided by n_samples times singular values to ensure 
                    # uncorrelated outputs with unit component-wise variances.
                    # Whitening will remove some information from the 
                    # transformed signal (the relative variance scales of the # components) but can sometime improve the predictive # 
                    # accuracy of the downstream estimators by making there 
                    # data respect some hard-wired assumptions.
                    'reducer__whiten': [True],                    
                },
                False # Enable the classifier
            )
        ]

    def get_models(self):
        """
            Return the various models defined in the __init__ function
        """
        return self.models