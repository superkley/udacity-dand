#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: ke
"""

import os
import xml.etree.ElementTree as ET

import pandas as pd
import seaborn as sns


def get_tag_v_value(tag):
    """
    get the value in attribute 'v' in the tag element
    """
    return tag.attrib['v']


def print_frequencies(df, name=None):
    """
    displays absolute and relative frequencies of the given feature in the dataframe
    """
    if name is None:
        name = df.columns[0]
    print("Absolute frequencies of '{0}':\n{1}\n".format(
        name,
        df[name]
    ))
    print("Relative frequencies of '{0}' [%]:\n{1}\n".format(
        name,
        df[name] / df[name].sum() * 100.0
    ))


def plot_frequencies(df, name=None):
    """
    plots absolute and relative frequencies of the given feature in the dataframe
    """
    if name is None:
        name = df.columns[0]
    fig = sns.plt.figure(figsize=(12, 3))
    df[name].plot.bar(ax=fig.add_subplot(121))
    sns.plt.title('Frequencies of {0}'.format(
        name
    ))
    (df[name] / df[name].sum()).plot.bar(ax=fig.add_subplot(122))
    sns.plt.title('Relative Frequencies of {0}'.format(
        name
    ))


def count_unique_items(file, filter_func, df_name=None, get_value_func=get_tag_v_value, tags=['node', 'way']):
    """
    find and count unique items by given criteria
    :return: dictionary of item occurrences or if df_name defined a one-column dataframe
    """
    items = {}
    with open(file, 'r') as f:
        for _, elem in ET.iterparse(f):
            if elem.tag in tags:
                for t in elem.iter('tag'):
                    if filter_func(t):
                        item = get_value_func(t)
                        if item not in items:
                            items[item] = 1
                        else:
                            items[item] += 1
    if df_name is None:
        return items
    else:
        return to_dataframe(df_name, items).sort_index()


def to_dataframe(name, freq_dict):
    """
    converts the dictionary to dataframe.
    :return: dataframe
    """
    return pd.DataFrame.from_dict(
        freq_dict,
        orient='index'
    ).rename(
        columns={0: name}
    ).sort_index()


def format_size(size, suffix='B'):
    """
    calculates and format human readable size

    source: http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    :return: formatted size
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(size) < 1024.0:
            return "%3.1f%s%s" % (size, unit, suffix)
        size /= 1024.0
    return "%.1f%s%s" % (size, 'Yi', suffix)


def get_file_size(file_path):
    """
    gets the file size of the given file path.

    :return: file size
    """
    return os.path.getsize(file_path)


def get_absolute_file_path(rel_file_path):
    """
    gets the absolute file path of the given relative file path
    :return: absolute file path
    """
    return os.path.abspath(rel_file_path)


def connect_to_mongodb(db, collection):
    """
    create connection to local mongodb database collection
    :return: connection to database collection
    """
    from pymongo import MongoClient
    client = MongoClient()
    db = client[db]
    return db[collection]


# initializations
sns.set(style='white', palette='muted', color_codes=True)
sns.set_context('notebook', font_scale=1.2, rc={'lines.linewidth': 1.2})
