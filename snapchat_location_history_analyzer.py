import folium
import json
import argparse
import typing

# local
import location_parser_helper


### Generates Folium map from JSON file containing coordinate data
def generate_folium_map(input_filename: str, output_filename : str):

    timestamps, latitudes, longitudes = location_parser_helper.get_location_history_coordinates(input_filename)

    map = folium.Map(zoom_start=12)

    for i in range(0, len(latitudes)):
        folium.Marker([latitudes[i], longitudes[i]],
                    popup=timestamps[i]).add_to(map)

    map.save(output_filename)

if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument(
        "-i", "--input-file", type=str, help="JSON file containing location history. Usually named location_history.json")
    argparse_parser.add_argument("-o", "--output-file", type=str, help="The html file containing the Folium map")

    argparse_args = argparse_parser.parse_args()

    generate_folium_map(argparse_args.input_file, argparse_args.output_file)