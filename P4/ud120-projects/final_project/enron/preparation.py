def get_characteristics(data):
    """
        Print several important metrics about the dataset
    """
    print 'Size of the dataset is : {}'.format(len(data))
    print "Number of features per person", len(data['SKILLING JEFFREY K'])
    enron_data_poi_array = []
    for x in data.values():
        if x['poi'] == True:
            enron_data_poi_array.append(x)
    print 'Number of POI in the dataset : {}'.format(len(enron_data_poi_array))

def get_max_Nan(data_dict, features_list):
    """
        Return the max number of NaN in the dataset
    """
    nbr_of_features = len(features_list)
    keys = data_dict.keys()
    max_na = 0
    for key in keys:
        nbr_of_NaN = 0
        for feature in features_list:
            data_dict[key][feature]
            value = data_dict[key][feature]
            if value=="NaN":
                nbr_of_NaN += 1
        if max_na < nbr_of_NaN:
            max_na = nbr_of_NaN
    print 'Max number of NaN per record', max_na
    return max_na

def get_person_highest_NaN(data_dict, features_list, max_na):
    """
        print the person having the highest NaN in the dataset
    """
    nbr_of_features = len(features_list)
    keys = data_dict.keys()
    threshold = max_na
    for key in keys:
        nbr_of_NaN = 0
        for feature in features_list:
            data_dict[key][feature]
            value = data_dict[key][feature]
            if value=="NaN":
                nbr_of_NaN += 1
        if nbr_of_NaN == threshold:
            print "Person with a high number of NaN :", key

def remove_outliers(data_dict):
    """
        Prune outliers from the dataset
    """
    data_dict.pop('TOTAL',0)
    data_dict.pop('LOCKHART EUGENE E',0)
    return data_dict

