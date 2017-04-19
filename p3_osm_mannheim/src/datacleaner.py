#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

"""
Module containing data cleaning functions used in data.py.
"""

city_mapping = {
    'Vierheim': 'Viernheim'
}

street_mapping = {
    'Strasse': 'Straße'
}

maxspeed_mapping = {
    'walk': '5',
    'none': '200'
}

operator_mapping = {
    'BASF': 'BASF SE',
    'DB Netz': 'DB Netz AG',
    'DB Post': 'DB Post AG',
    'Deutsche Telekom': 'Deutsche Telekom AG',
    'EnBW': 'EnBW AG',
    'Hall': 'Hall Tabakwaren',
    'RNV': 'RNV GmbH',
    'Rhein-Neckar-Verkehr GmbH': 'RNV GmbH',
    'MVV': 'MVV Energie AG',
    'MVV Energie': 'MVV Energie AG'
}


def correct_max_speed(value):
    """
    correct the max speed using mappings
    :return: corrected max speed
    """
    return int(correct_by_mappings(value, maxspeed_mapping))


def correct_city_names(value):
    """
    correct city names by mapping.
    :return: corrected city name
    """
    return correct_by_mappings(value, city_mapping)


def correct_street_names(value):
    """
    correct street names by mapping.
    :return: corrected street name
    """
    return correct_by_mappings(value, street_mapping, match_whole_word=False)


def correct_operator_names(value):
    """
    correct operator names by mapping.
    :return: corrected operator name
    """
    return correct_by_mappings(value, operator_mapping)


def correct_by_mappings(name, mapping, match_whole_word=True):
    """
    correct the given name using mappings
    :return: corrected name
    """
    for key in mapping.iterkeys():
        if match_whole_word:
            if name == key:
                return mapping[key]
        else:
            if re.search(key, name):
                name = re.sub(key, mapping[key], name)
    return name
