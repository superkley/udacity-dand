#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow


def parse_args():
    """
    parses commmand-line options for osm file, sample file and k
    :return: dictionary of options
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file_path', default='map.osm',
                        help='file path to the input map osm file')
    parser.add_argument('-o', dest='output_file_path', default='sample.osm',
                        help='file path to the output sample osm file')
    parser.add_argument('-k', dest='k', type=int, default=10,
                        help='take every k-th top level element (sample factor)')
    return parser.parse_args()


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag
    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


if __name__ == "__main__":
    options = parse_args()
    OSM_FILE = options.input_file_path
    SAMPLE_FILE = options.output_file_path
    k = options.k

    with open(SAMPLE_FILE, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')
        # Write every kth top level element
        for i, element in enumerate(get_element(OSM_FILE)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))
        output.write('</osm>')
