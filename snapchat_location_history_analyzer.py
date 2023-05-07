import folium
import json

# local
import location_parser_helper

# TODO: Add argparse support for json filename

def main():

    timestamps, latitudes, longitudes = location_parser_helper.get_location_history_coordinates("location_history.json")

    map = folium.Map(zoom_start=12)

    for i in range(0, len(latitudes)):
        folium.Marker([latitudes[i], longitudes[i]],
                    popup=timestamps[i]).add_to(map)

    map.save("snapchat-map.html")

if __name__ == "__main__":
    main()