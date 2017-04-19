"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Crescent", "West", "South", "East", "North", "Vista",
            "Gardens", "Circle", "Gate", "Heights", "Park", "Way", "Mews", "Keep", "Westway", "Glenway",
            "Queensway", "Wood", "Path"]

mapping = {"Ave": "Avenue",
           "St.": "Street",
           "Rd.": "Road",
           "StreetE": "Street East",
           "Robertoway": "Roberto Way"
           }


def audit_street_type(street_types, street_name):
    """Update dictionary of street names and mapping type"""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    with open(osmfile, "r") as osm_file:
        street_types = defaultdict(set)
        for _, elem in ET.iterparse(osm_file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if is_street_name(tag):
                        audit_street_type(street_types, tag.attrib['v'])
    return street_types


def update_name(name, mapping):
    """Replace and return new name from street name mapping."""
    for key in mapping.iterkeys():
        if re.search(key, name):
            name = re.sub(key, mapping[key], name)

    return name


def test():
    st_types = audit('sample.osm')
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()
