# -*- coding: utf-8 -*-
#!/usr/bin/python

""" 
    starter code for exploring the Enron dataset (emails + finances) 
    loads up the dataset (pickled dict of dicts)

    the dataset has the form
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person
    you should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))
execfile("../final_project/poi_email_addresses.py")
execfile("../tools/feature_format.py")

print "Number of data points (people) in the dataset", len(enron_data)
print "Number of features per person", len(enron_data['SKILLING JEFFREY K'])
count = 0
for user in enron_data:
    if enron_data[user]['poi'] == True:
        count+=1
print "POI emails ? ", len(poiEmails())
fo = open('../final_project/poi_names.txt','r')
fr = fo.readlines()
print "How many POIs are there in the E+F dataset? ", len(fr[2:])
fo.close()
#print enron_data.keys()
print enron_data['SKILLING JEFFREY K'].keys()
print "What is the total value of the stock belonging to James Prentice? ", enron_data['PRENTICE JAMES']['total_stock_value']
print "How many email messages do we have from Wesley Colwell to persons of interest? ", enron_data['COLWELL WESLEY']['from_this_person_to_poi']
print "What’s the value of stock options exercised by Jeffrey Skilling? ", enron_data['SKILLING JEFFREY K']['exercised_stock_options']
print "How is an unfilled feature denoted? ", enron_data['FASTOW ANDREW S']['deferral_payments']
count_salary = 0
count_email = 0
for key in enron_data.keys():
    if enron_data[key]['salary'] != 'NaN':
        count_salary+=1
    if enron_data[key]['email_address'] != 'NaN':
        count_email+=1
print "How many folks in this dataset have a quantified salary? What about a known email address? ", count_salary, count_email
count_NaN_tp = 0
for key in enron_data.keys():
    if enron_data[key]['total_payments'] == 'NaN':
        count_NaN_tp+=1
print 'How many people in the E+F dataset (as it currently exists) have “NaN” for their total payments? What percentage of people in the dataset as a whole is this?', count_NaN_tp, float(count_NaN_tp)/len(enron_data.keys()) * 100
count_NaN_tp = 0
for key in enron_data.keys():
    if enron_data[key]['total_payments'] == 'NaN' and enron_data[key]['poi'] == True :
        print 
        count_NaN_tp+=1
print 'How many POIs in the E+F dataset have “NaN” for their total payments? What percentage of POI’s as a whole is this?', count_NaN_tp, float(count_NaN_tp)/len(enron_data.keys())*100
print "If a machine learning algorithm were to use total_payments as a feature, would you expect it to associate a “NaN” value with POIs or non-POIs?", len(enron_data.keys())
count = 0
for user in enron_data:
    if enron_data[user]['poi'] == True and enron_data[user]['total_payments'] == 'NaN':
        count+=1
print 'What is the new number of people of the dataset? What is the new number of folks with “NaN” for total payments?', count
