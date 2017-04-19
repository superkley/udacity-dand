#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint

"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""


def get_user(element):
    """
    counts unique user uids
    """
    user = set()
    if "uid" in element.attrib:
        user.add(element.attrib["uid"])
    return user


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        users.update(get_user(element))
    return users


def test():
    users = process_map('sample.osm')
    pprint.pprint(len(users))


if __name__ == "__main__":
    test()
