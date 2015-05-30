# -*- coding: utf-8 -*-
#!/usr/bin/python
from sklearn import preprocessing
from sklearn.preprocessing import Imputer

def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """
    fraction = 0.

    if all_messages == 'NaN':
        return fraction
    
    if poi_messages == 'NaN':
        poi_messages = 0
    
    fraction = float(poi_messages)/float(all_messages)

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
        fraction_from_poi = computeFraction(from_poi_to_this_person, to_messages)
        data_point["fraction_from_poi"] = fraction_from_poi

        from_this_person_to_poi = data_point["from_this_person_to_poi"]
        from_messages = data_point["from_messages"]
        fraction_to_poi = computeFraction(from_this_person_to_poi, from_messages)
        data_point["fraction_to_poi"] = fraction_to_poi

    features_list.append('fraction_from_poi')
    features_list.append('fraction_to_poi')

    return data_dict, features_list

def scale(features):    
    """
        scale the features.
    """
    features = preprocessing.MinMaxScaler().fit_transform(features)
    return features

def impute(features, strategy='mean'):    
    """
        Impute the missing value by a strategy (mean, median)
        default strategy is 'mean'
    """
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imputed_features = imp.fit_transform(features)
    return imputed_features