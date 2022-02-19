import folium
import json

with open("location_history.json") as location_history_json_file:
    raw_loc_history_json_data = json.load(location_history_json_file)

 # The location history file contains multiple subfields
 # They are: 'Frequent Locations', 'Latest Location', 'Home & Work', 'Daily Top Locations', and 'Location History' (the one we're interested in)
timestamp_location_history = raw_loc_history_json_data['Location History']
timestamps, latitudes, longitudes = [], [], []

for entry in timestamp_location_history:

    # Each entry looks something like:
    # {'Time': '2021/09/02 20:37:47 UTC', 'Latitude, Longitude': '37.332 ± 39.66 meters, -121.884 ± 39.66 meters'}

    timestamps.append(entry['Time'])

    lat_with_margin, lon_with_margin = entry['Latitude, Longitude'].split(",")

    latitudes.append(lat_with_margin.split()[0])
    longitudes.append(lon_with_margin.split()[0])

if not (len(timestamps) == len(longitudes) == len(latitudes)):
    print("Error parsing timestamped LAT/LON data. Data dimensions did not match up")
    exit(1)

map = folium.Map(zoom_start=12)

for i in range(0, len(latitudes)):
    folium.Marker([latitudes[i], longitudes[i]], popup=timestamps[i]).add_to(map)

map.save("map.html")