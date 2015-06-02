# -*- coding: utf-8 -*-
#!/usr/bin/python
from sklearn import preprocessing
from sklearn.preprocessing import Imputer

def compute_fraction( numerator, denominator ):
    """ compute a basic fraction with fromat conversion
   """
    fraction = 0.

    if denominator == 'NaN':
        return fraction
    
    if numerator == 'NaN':
        numerator = 0
    
    fraction = float(numerator)/float(denominator)

    return fraction

def create_email_ratio(data_dict, features_list):
    """ 
        calculate the ratio/percentage of emails received or sent from/to a 
        POI's.
    """
    for name in data_dict:

        data_point = data_dict[name]

        from_poi_to_this_person = data_point["from_poi_to_this_person"]
        to_messages = data_point["to_messages"]
        fraction_from_poi = compute_fraction(from_poi_to_this_person, to_messages)
        data_point["fraction_from_poi"] = fraction_from_poi

        from_this_person_to_poi = data_point["from_this_person_to_poi"]
        from_messages = data_point["from_messages"]
        fraction_to_poi = compute_fraction(from_this_person_to_poi, from_messages)
        data_point["fraction_to_poi"] = fraction_to_poi

    features_list.append('fraction_from_poi')
    features_list.append('fraction_to_poi')

    return data_dict, features_list

def create_financial_ratio(data_dict, features_list):
    """
        calculate the financial ration feature
    """
    payment_features = ['salary', 'deferral_payments','bonus', 'expenses',
                        'loan_advances', 'other', 'director_fees',
                        'deferred_income', 'long_term_incentive']

    stock_features = ['exercised_stock_options', 'restricted_stock', 
                      'restricted_stock_deferred']

    for name in data_dict:
        data_point = data_dict[name]
        # compute for the payment features
        ratio = "total_payments"
        denominator = data_point[ratio]
        for item in payment_features:
            key = 'fraction_{0}_{1}'.format(item, ratio)
            data_point[key] = compute_fraction(data_point[ratio], denominator)            
        # compute for the stocks features
        ratio = "total_stock_value"
        denominator = data_point[ratio]
        for item in stock_features:
            key = 'fraction_{0}_{1}'.format(item, ratio)
            data_point[key] =compute_fraction(data_point[ratio], denominator)

    # append the new payment's feature in the features list
    for payment in payment_features:
        features_list.append('fraction_{0}_{1}'.format(payment, 'total_payments'))

    # append the new stock's feature in the features list
    for stock in stock_features:
        features_list.append('fraction_{0}_{1}'.format(stock, 'total_stock_value'))

    return data_dict, features_list

def scale(features):    
    """
        scale the features.
    """
    features = preprocessing.MinMaxScaler().fit_transform(features)
    return features

def standardize(features):
    """
        Standardization refers to shifting the distribution of each attribute 
        to have a mean of 0 and a standard deviation of 1
    """
    features = preprocessing.scale(features)
    return features

def impute(features, strategy='mean'):    
    """
        Impute the missing value by a strategy (mean, median)
        default strategy is 'mean'
    """
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imputed_features = imp.fit_transform(features)
    return imputed_features