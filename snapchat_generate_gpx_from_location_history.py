import lxml.etree
import lxml.builder
import datetime
import os
import typing
import pdb

# locals
import location_parser_helper

# TODO: Parameterize for both input and output file
output_file = "snapchat.xml"

xml_header = """<?xml version="1.0" encoding="utf-8"?>"""

#elem_maker = lxml.builder.ElementMaker(namespace="http://www.topografix.com/GPX/1/1", nsmap={"xsi" : "http://www.w3.org/2001/XMLSchema-instance"})
elem_maker = lxml.builder.ElementMaker()

# TODO: Add bounds
timestamps, latitudes, longitudes = location_parser_helper.get_location_history_coordinates("location_history.json")

# The GPX file standard requires that you specify the coordinate bounds
min_lat, min_lon, max_lat, max_lon = min(latitudes), min(longitudes), max(latitudes), max(longitudes)

gpx_document = elem_maker.gpx( elem_maker.metadata( elem_maker.copyright(author="Raleigh Littles"), elem_maker.time(str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"))), elem_maker.keywords("github.com/raleighlittles"), elem_maker.bounds(minlat=str(min_lat), minlon=str(min_lon), maxlat=str(max_lat), maxlon=str(max_lon))), xmlns="http://www.topografix.com/GPX/1/1", version="1.1", creator=str(os.path.basename(__file__)))

gpx_document.append(elem_maker.wpt(elem_maker.cmt(timestamps[0]), lat=latitudes[0], lon=longitudes[0]))

#print lxml.etree.tostring(the_doc, pretty_print=True)

with open(output_file, 'w') as f:
    f.write(str(xml_header))
    f.write(str(lxml.etree.tostring(gpx_document)))
    f.close()