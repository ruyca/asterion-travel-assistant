# nearest_lyf.py

import json
from geopy.distance import geodesic

def calculate_distance(coord1: tuple, coord2: tuple) -> float:
    """Calculates the distance in KM between two latitude 
    and longitude coordinates"""

    return round(geodesic(coord1, coord2).kilometers, 2)


def find_closest_locations(user_coords, max_distance):

    lyf_locations_path="lyf_locations.json"

    # Read the JSON file
    with open(lyf_locations_path, 'r') as file:
        locations_data = json.load(file)
    
    # List to store tuples of (location_name, distance)
    locations_with_distance = []

    # Iterate over each country in the JSON file
    for country_data in locations_data:
        for country, locations in country_data.items():
            # Iterate over each location in the country
            for location in locations:
                loc_coords = (float(location['location']['latitude']), float(location['location']['longitude']))
                distance = calculate_distance(user_coords, loc_coords)
                
                # Only consider the location if it's within the max_distance
                if distance <= max_distance:
                    locations_with_distance.append((location['name'], location['Address'], distance, location['photo']))
    
    # Sort locations by distance (ascending order)
    locations_with_distance.sort(key=lambda x: x[2])
    
    # Get the top 3 closest locations
    closest_locations = locations_with_distance[:3]
    
    return closest_locations

