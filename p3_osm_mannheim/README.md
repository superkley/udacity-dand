# Data Wrangling with MongoDB: Wrangle OpenStreetMap Data

* Udacity Data Analyst Nanodegree: Project 3
* Author: Ke Zhang
* Submission Date: 2017-04-02 (Revision 2)

## Map Area

* Mannheim, Baden-W¨¹rttemberg, Germany
* Link to the map position: [Mannheim on OpenStreetMap](https://tools.wmflabs.org/wiwosm/osm-on-ol/kml-on-ol.php?lang=de&uselang=de&params=49.483611111111_N_8.4630555555556_E_region%3ADE-BW_type%3Acity%28305780%29&title=Mannheim&zoom=10&lat=49.50051&lon=8.50208&layers=B0000000FTTTF)


## File Listing

* Report Files:
	* ./p3_osm_mannheim_report.html: report in HTML format
	* ./p3_osm_mannheim_report.pdf: the same report file in PDF format
	* ./p3_osm_mannheim_complete.html: the complete Jupyter ipynb output in HTML format
* Source Files:
	* ./src/p3_osm_mannheim.ipynb: the original ipynb file
	* ./src/p3_osm_mannheim.py: functions and code used in ipynb notebook
	* ./src/data.py: modified script to convert OSM XML file to JSON format
	* ./src/datacleaner.py: module containing data cleaning functions used in data.py.
	* ./src/sample.py: modified script to extract sample entries from OSM XML file
	* ./src/mapparser.py: extracts tag names and their frequencies
	* ./src/tags.py: checks k values in tag-tags
	* ./src/users.py: counts unique user ids
	* ./src/audit.py: audits and fixes street names
* Sample Data:
	* ./data/sample.osm

	
## References

* [Udacity Website](udacity.com)
* [Pandas Documentation](http://pandas.pydata.org/pandas-docs/stable/)
* [OpenStreetMap XML Structure](https://wiki.openstreetmap.org/wiki/OSM_XML](https://wiki.openstreetmap.org/wiki/OSM_XML)
* [OpenStreetMap Map Elements](https://wiki.openstreetmap.org/wiki/Elements](https://wiki.openstreetmap.org/wiki/Elements)
* [MongoDB Manual](https://docs.mongodb.com/manual/)
* [Mannheim OpenData](https://mannheim.opendatasoft.com/explore)
* [PyMongo Documentation](https://api.mongodb.com/python/current/)


