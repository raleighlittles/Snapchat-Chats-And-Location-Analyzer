import json
import pdb
import typing

# Each entry looks something like:
# {'Time': '2021/09/02 20:37:47 UTC', 'Latitude, Longitude': '37.332 ± 39.66 meters, -121.884 ± 39.66 meters'}

def get_location_history_coordinates(location_history_filename : str, with_timestamps=True) -> typing.List:
    with open("location_history.json") as location_history_json_file:
        raw_loc_history_json_data = json.load(location_history_json_file)

    # The location history file contains multiple subfields
    # They are: 'Frequent Locations', 'Latest Location', 'Home & Work', 'Daily Top Locations', and 'Location History' (the one we're interested in)
    timestamp_location_history = raw_loc_history_json_data['Location History']
    timestamps, latitudes, longitudes = [], [], []

    for entry in timestamp_location_history:
        timestamps.append(entry['Time'])

        lat, lon = extract_lat_long_entry(entry)
        latitudes.append(lat)
        longitudes.append(lon)

    if not (len(timestamps) == len(longitudes) == len(latitudes)):
        raise Exception("Error parsing timestamped LAT/LON data. Data dimensions did not match up.")
    
    return [timestamps, latitudes, longitudes]

def extract_lat_long_entry(entry : typing.List) -> tuple:

    lat_with_margin, lon_with_margin = entry['Latitude, Longitude'].split(",")

    # Interesting bug here in the `split()` behavior. Calling `split()` with no arguments is the same as calling `split(" ")`,
    # but if you DON'T provide the argument, `split()` will automatically remove empty strings from the result
    return tuple([lat_with_margin.split(" ")[0], lon_with_margin.split()[0]])