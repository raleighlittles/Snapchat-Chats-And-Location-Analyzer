import argparse
import datetime
import lxml.builder
import lxml.etree
import os
import pdb
import socket
import typing

# locals
import location_parser_helper


def generate_location_history_gpx_file(input_json_filename: str, output_gpx_filename: str):

    # Couldn't figure out a way to have LXML automatically add the header
    xml_header = """<?xml version="1.0" encoding="utf-8"?>"""

    elem_maker = lxml.builder.ElementMaker()

    timestamps, latitudes, longitudes = location_parser_helper.get_location_history_coordinates(
        input_json_filename)

    # The GPX file standard requires that you specify the coordinate bounds
    min_lat, min_lon, max_lat, max_lon = min(latitudes), min(
        longitudes), max(latitudes), max(longitudes)

    gpx_document = elem_maker.gpx(elem_maker.metadata(elem_maker.copyright(author=socket.gethostname()), elem_maker.time(str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"))), elem_maker.keywords("https://github.com/raleighlittles/Snapchat-Chats-And-Location-Analyzer"),
                                  elem_maker.bounds(minlat=str(min_lat), minlon=str(min_lon), maxlat=str(max_lat), maxlon=str(max_lon))), xmlns="http://www.topografix.com/GPX/1/1", version="1.1", creator=str(os.path.basename(__file__)))

    for i in range(0, len(timestamps)):
        gpx_document.append(elem_maker.wpt(elem_maker.cmt(
            timestamps[i]), lat=latitudes[i], lon=longitudes[i]))

    with open(output_gpx_filename, 'w') as f:
        f.write(str(xml_header))
        f.write(lxml.etree.tostring(gpx_document, pretty_print=True).decode())
        f.close()


if __name__ == "__main__":

    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-i", "--input-file", type=str,
                                 help="JSON file containing location history. Usually named location_history.json")
    argparse_parser.add_argument(
        "-o", "--output-file", type=str, help="The name of the GPX file")

    argparse_args = argparse_parser.parse_args()

    generate_location_history_gpx_file(
        argparse_args.input_file, argparse_args.output_file)
