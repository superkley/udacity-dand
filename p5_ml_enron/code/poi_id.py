#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

# custom defined functions (shared by .ipynb and poi_id.py)
import p5_ml_enron as prj

sys.path.append("../tools/")
from tester import dump_classifier_and_data,test_classifier

# load data set as dataframe
df = prj.pkl_to_df('./final_project_dataset.pkl')


###########################################################################
### Task 1: Select what features you'll use.                              #
###########################################################################
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

# selected features: numeric columns. without email_addresses.
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances',
                 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value',
                 'expenses', 'exercised_stock_options', 'long_term_incentive', 'other',
                 'restricted_stock', 'director_fees', 'to_messages', 'from_poi_to_this_person',
                 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

###########################################################################
### Task 2: Remove outliers                                               #
###########################################################################

# reason: empty feature values
df = df.drop(['LOCKHART EUGENE E'])

# reason: total sum, not a person
df = df.drop(['TOTAL'])

# reason: agency name, not a person
df = df.drop(['THE TRAVEL AGENCY IN THE PARK'])

# reason: corrupted data, no poi
df = df.drop(['BELFER ROBERT'])
df = df.drop(['BHATNAGAR SANJAY'])

# drop unused email address column
df = df.drop('email_address', axis=1)

###########################################################################
### Task 3: Create new feature(s)                                         #
###########################################################################

# copy original features for evaluation
original_df = df.copy()

# total amount of money of a person
df['total_assets'] = df['total_payments'] + df['total_stock_value']

# total stock value vs total payments ratio
df['stock_payments_ratio'] = prj.get_ratio(
    df['total_stock_value'],
    df['total_payments']
)

# other vs total payments ratio
df['other_payments_ratio'] = prj.get_ratio(
    df['other'],
    df['total_payments']
)

# messages sent to vs received from a poi ratio
df['poi_messages_ratio'] = prj.get_ratio(
    df['from_this_person_to_poi'] + df['from_poi_to_this_person'],
    df['to_messages'] + df['from_messages']
)

# add new features to features list
features_list.extend(['total_assets', 'stock_payments_ratio',
                      'other_payments_ratio', 'poi_messages_ratio'])

### handle missing values (required for classifiers)
# replace missing ratios with median
prj.fillna_by_median(df['stock_payments_ratio'])
prj.fillna_by_median(df['other_payments_ratio'])
prj.fillna_by_median(df['poi_messages_ratio'])

# set other missing numbers to with 0
df = df.fillna(0)

###########################################################################
### Task 4: Try a varity of classifiers                                   #
###########################################################################
### Please name your classifier clf for easy export below.

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

###########################################################################
### Task 5: Tune your classifier to achieve better than .3 precision and  #
### recall  using our testing script.                                     #
###########################################################################
### Check the tester.py script in the final project folder for details on
### the evaluation method, especially the test_classifier function. Because
### of the small size of the dataset, the script uses stratified shuffle
### split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Validate model precision, recall and F1-score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

clf = Pipeline(steps=[
     ('scale', MinMaxScaler()),
     ('reduce', PCA(n_components=2, random_state=42)),
     ('classify', LogisticRegression(C=10, class_weight='balanced', random_state=42, solver='liblinear'))
])

### evaluate both the current and the original feature set
# with new features
my_dataset = prj.df_to_dict(df)
test_classifier(clf, my_dataset, features_list)
# original feature set
original_df = original_df.fillna(0)
original_features_list = ['poi'] + list(original_df.drop('poi', axis=1).columns)
original_dataset = prj.df_to_dict(original_df)
test_classifier(clf, original_dataset, original_features_list)
# => the original features set outperforms the final one

###########################################################################
### Task 6: Dump your classifier, dataset, and features_list so anyone    #
### can check your results.                                               #
###########################################################################
### You do not need to change anything below, but make sure that
### the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

# uses original data set and features list
dump_classifier_and_data(clf, original_dataset, original_features_list)
