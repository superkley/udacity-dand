#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import codecs
import json
import datacleaner as cleaner

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: 'node',
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB.

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.

In particular the following things should be done:
- you should process only 2 types of top level tags: 'node' and 'way'
- all attributes of 'node' and 'way' should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for 'way' specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@,\. \t\r\n]')
CREATED = ["version", "changeset", "timestamp", "user", "uid"]

def parse_args():
    """
    parses commmand-line options for osm file
    :return: dictionary of options
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file_path', default='map.osm',
                        help='file path to the input map osm file')
    return parser.parse_args()


def shape_element(elem):
    """
    validate and format node and way elements
    """
    if elem.tag in ['node', 'way']:
        node = {'created': {}, 'type': elem.tag}
        for key in elem.attrib:
            if key in CREATED:
                node['created'][key] = elem.attrib[key]
            elif key == 'lat':
                # assumes that coordinate is always complete
                node['pos'] = [float(elem.attrib['lat']), float(elem.attrib['lon'])]
            else:
                # add other keyvalues to element
                node[key] = elem.attrib[key]
        for tag in elem.iter('tag'):
            k = tag.attrib['k'].strip()
            v = tag.attrib['v'].strip()
            if problemchars.search(k):
                # skipped
                continue
            elif k.startswith('addr:'):
                addr = k.split(':')
                if len(addr) == 2:
                    if 'address' not in node:
                        node['address'] = {}
                    if k == 'addr:city':
                        v = cleaner.correct_city_names(v)
                    elif k == 'addr:street':
                        v = cleaner.correct_street_names(v)
                    node['address'][addr[1]] = v
            else:
                if k == 'operator':
                    v = cleaner.correct_operator_names(v)
                elif k == 'maxspeed':
                    v = cleaner.correct_max_speed(v)
                node[k] = v
            node['node_refs'] = [nd.attrib['ref'] for nd in elem.iter('nd')]
        return node
    else:
        return None


def process_map(file_in, pretty=False, generate_array_result=True):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                if generate_array_result:
                    data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == "__main__":
    options = parse_args()
    process_map(options.input_file_path, generate_array_result=False)
