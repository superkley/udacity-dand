#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Custom functions used in .ipynb and poi_id.py.

@author: ke
"""

# load libraries
import pickle
import sys

from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, f_classif, f_regression
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline

sys.path.append('../tools/')
from tester import test_classifier

# initialize context and global options
sns.set(style='white', palette='muted', color_codes=True)
sns.set_context('notebook', font_scale=1.2, rc={'lines.linewidth': 1.2})
# disable chained assignment warning
pd.options.mode.chained_assignment = None
random_state = 42
# default max features number
max_features = 10


def split_by(df, feature):
    """
    splits records by the given boolean column e.g. 'poi'
    :return: splitted records as a tuple
    """
    return [
        df[df[feature] == True],
        df[df[feature] == False]
    ]


def print_summary(df):
    """
    prints summary of the project dataset with basic descriptions and statistics.
    """
    poi_df, npoi_df = split_by(df, 'poi')

    print('# total: {}'.format(len(df)))
    print('# poi: {}'.format(len(poi_df)))
    print('# non-poi: {}'.format(len(npoi_df)))
    print('# features: {}'.format(len(df.columns.values)))
    print('poi-total ratio: {0:.2f}%'.format(
        len(poi_df) * 100.0 / len(df))
    )
    print('poi-non-poi ratio: {0:.2f}%'.format(
        len(poi_df) * 100.0 / len(npoi_df))
    )
    print('\ntop 5 total payments:\n{}'.format(
        df['total_payments'].sort_values(ascending=False).head()
    ))
    print('\ntop 5 total stock values:\n{}'.format(
        df['total_stock_value'].sort_values(ascending=False).head()
    ))
    print('\ntop 5 from messages:\n{}'.format(
        df['from_messages'].sort_values(ascending=False).head()
    ))
    print('\ntop 5 from other payments:\n{}'.format(
        df['other'].sort_values(ascending=False).head()
    ))
    print('\ntop 5 having null values:\n{}'.format(
        df.T.isnull().sum().sort_values(ascending=False).head()
    ))


def fillna_by_median(var):
    """
    fills missing values with median of the column.
    """
    var.fillna(var.median(), inplace=True)


def has_value(var):
    """
    checks if the given value is not None or,0.
    """
    return (var != 0) & (var is not None)


def get_ratio(var1, var2):
    """
    calcualates the ratio of the two variables when both values are not none or 0.
    :return: ratio of the two variables
    """
    valid = has_value(var1) & has_value(var2)
    return var1[valid] / var2[valid]


def normalize(df):
    """
    scales the column values to 0 to 1.
    :return: a new dataframe with scaled values
    """
    scaler = MinMaxScaler()
    return pd.DataFrame(
        scaler.fit_transform(df.values),
        columns=df.columns,
        index=df.index
    )


def pkl_to_dict(pkl_path):
    """
    loads project data from prepared pickle file.
    :return: project data as dictionary
    """
    with open(pkl_path, 'r') as f:
        return pickle.load(f)


def pkl_to_df(pkl_path):
    """
    loads project data from prepared pickle file.
    :return: project data as dataframe
    """
    dict = pkl_to_dict(pkl_path)
    df = pd.DataFrame.from_dict(dict, orient='index')
    df.replace(['NaN'], [None], inplace=True)
    return df


def df_to_dict(df):
    """
    transforms dataframe back to dict
    :return: dict of the given df
    """
    return df.T.to_dict()


def merge_dicts(*dicts):
    """
    merge dictionaries together
    :return: merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def plot_correlation_matrix(df):
    """
    plots pearson correlation heatmap of the dataframe
    """
    sns.FacetGrid(df, size=7).map_dataframe(
        lambda data,
               color: sns.heatmap(
            data.corr().abs(),
            linewidths=1,
            cmap="YlGnBu"
        )
    )
    sns.plt.title("Pearson Correlation Matrix")


def split_features_labels(df):
    """
    splits the given dataframe to features and lables ('poi') columns.
    :return: tuple of features and labels
    """
    return [df.drop('poi', axis=1), df['poi']]


def get_train_test_split(df, test_size=.3):
    """
    splits records to train and test partitions (uses the same parameters as in the 'tester.py')
    :return: an array containing: features train, features test, labels train, labels test
    """
    features, target = split_features_labels(df)
    return train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target
    )


def rank_features(features, scores, descending=True, n=max_features):
    """
    sorts and cuts features by scores.
    :return: array of [feature name, score] tuples
    """
    return sorted(
        [[f, s] for f, s in zip(features, scores) if s],
        key=lambda x: x[1],
        reverse=descending
    )[:n]


def select_features_by_decision_tree(features, labels):
    """
    selects the top features by decision tree algorithm.
    :return: array of [feature name, score] tuples
    """
    clf = DecisionTreeClassifier()
    clf.fit(features, labels)
    return rank_features(
        features,
        clf.feature_importances_
    )


def select_features_by_kbest(features, labels):
    """
    selects the top features by selectkbest.
    :return: array of [feature name, score] tuples
    """
    kbest = SelectKBest()
    kbest.fit(features, labels)
    return rank_features(
        features,
        kbest.scores_
    )


def select_features_by_pca(features, labels):
    """
     selects the top features by pca.
    :return: array of [feature name, score] tuples
    """
    pca = PCA(n_components=max_features)
    pca.fit(features, labels)
    return rank_features(
        features,
        pca.explained_variance_ratio_
    )


def select_features_by_rfe(features, labels):
    """
    selects the top features by rfe.
    :return: array of [feature name, score] tuples
    """
    rfe = RFE(LogisticRegression())
    rfe.fit(features, labels)
    return rank_features(
        features,
        rfe.ranking_,
        descending=False
    )


def create_pipeline(clf):
    """
    creates a pipeline using the template: scale, reduce and classify
    :return: the created pipeline
    """
    clf.random_state = random_state
    return Pipeline(steps=[
        ('scale', MinMaxScaler()),
        ('reduce', SelectKBest()),
        ('classify', clf)
    ])


def train_pipeline(df, pipe, clf_params, folds=10):
    """
    trains the  pipeline by the given classifier and predefined dimension reducer parameters.
    :return: tuple of best estimator and best parameters
    """
    features, target = split_features_labels(df)
    # params to tune, reducers: pca, rfe and kbest
    max_n = features.columns.size
    params = create_pipeline_params(clf_params, max_n)
    # use stratified splits
    folder = StratifiedShuffleSplit(folds, test_size=.3, train_size=.7)
    folder.random_state = random_state
    # use f1 scoring to train combined precision and recall metrics
    grid = GridSearchCV(pipe, cv=folder, n_jobs=4, param_grid=params, scoring='f1')
    grid.fit(features, target)
    return [grid.best_estimator_, grid.best_params_]


def get_base_class_name(obj):
    """
    returns the base class name of the given object
    :return: base class name
    """
    return obj.__class__.__name__.rsplit('.', 1)[-1]


def print_dictionary(dict, fill=4):
    """
    pretty print dictionary content.
    """
    for k, v in dict.items():
        print('{0: <{1}}{2}={3}'.format(
            ' ',
            fill,
            k,
            v
        ))


def filter_by_prefix(dict, prefix):
    """
    filters dictionary entries by key prefixes.
    :return: a new filtered dictionary
    """
    return {k: v for k, v in dict.items() if k.startswith(prefix)}


def evaluate_pipeline(df, pipe_result):
    """
    evalutes the trained pipeline results. Displays the algorithm name, parameters, performance metrics
    of all records, and for the train, test partitions used in 'tester.py'
    """
    features, target = split_features_labels(df)
    pipeline, params = pipe_result
    clf = pipeline.named_steps['classify']
    reducer = pipeline.named_steps['reduce']
    if get_base_class_name(reducer) == 'PCA':
        selected = rank_features(features, reducer.explained_variance_ratio_)
    else:
        selected = rank_features(features, reducer.get_support())
    features_list = [x[0] for x in selected]
    lbl = 'Estimator: {}'.format(get_base_class_name(clf))
    print('{1:=<{2}}\n{0}\n{1:=<{2}}'.format(lbl, '=', len(lbl)))
    print('> selected features: {}'.format(features_list))
    print('> scaler params:')
    print_dictionary(filter_by_prefix(params, 'scale'))
    print('> dimension reducer params:')
    print_dictionary(filter_by_prefix(params, 'reduce'))
    print('> estimator params:')
    print_dictionary(filter_by_prefix(params, 'classify'))
    print('\nPerformance metrics (train):')
    print_metrics(pipeline, features, target)
    print('Performance metrics (tester.py):')
    run_tester_check(df, pipeline, list(features.columns))


def run_tester_check(df, clf, features_list):
    """
    check tester.py test_classifier metrics.
    """
    my_dataset = df_to_dict(df)
    test_classifier(clf, my_dataset, ['poi'] + features_list)


def print_metrics(clf, features, labels):
    """
    predicts and prints the performance metrics such as accuracy, precision, recall and f1.
    """
    predictions = clf.predict(features)
    print('> accuracy={0:.2f}, precision={1:.2f}, recall={2:.2f}, f1={3:.2f}\n'.format(
        accuracy_score(labels, predictions),
        precision_score(labels, predictions),
        recall_score(labels, predictions),
        f1_score(labels, predictions)
    ))


def create_pipeline_params(clf_params, max_n):
    """
    creates grid search parameters.
    :return:parameters for the pipeline grid search.
    """
    prefixed_clf_params = {'classify__' + k: v for k, v in clf_params.items()}
    scaler_params = {
        'scale': [MinMaxScaler()]
    }
    return [
        merge_dicts(scaler_params, {
            'reduce': [PCA(random_state=random_state)],
            'reduce__n_components': range(1, max_n)
        }, prefixed_clf_params),
        merge_dicts(scaler_params, {
            'reduce': [RFE(LogisticRegression())],
            'reduce__n_features_to_select': range(1, max_n),
        }, prefixed_clf_params),
        merge_dicts(scaler_params, {
            'reduce': [SelectKBest()],
            'reduce__k': range(1, max_n),
            'reduce__score_func': [
                chi2,
                f_classif,
                f_regression
            ]
        }, prefixed_clf_params)
    ]
