from overpy import Overpass
import requests

#find neigboihood cities
def get_towns_in_radius(lat, lon, radius):
    overpass = Overpass()

    # Calculate bounding box based on radius (approximation)
    lat_deg_km = 110.574
    lon_deg_km = 111.32 * abs(lon)
    lat_delta = radius / lat_deg_km
    lon_delta = radius / lon_deg_km

    min_lat = lat - lat_delta
    max_lat = lat + lat_delta
    min_lon = lon - lon_delta
    max_lon = lon + lon_delta

    # Query for places within bounding box
    query = f"""
    node["place"]({min_lat},{min_lon},{max_lat},{max_lon});
    out;
    """
    result = overpass.query(query)
    # Filter results to towns/cities
    towns = []
    for node in result.nodes:
        if 'place' in node.tags:
            place_type = node.tags['place']
            if place_type in ['town']:
                towns.append(node.tags.get('name', 'Unnamed'))
    return towns

# Example: Retrieving data about a given town
def get_neighbourhood_towns(place_name, radius):
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    response = requests.get(url)
    data = response.json()
    lat, lon = data[0]["lat"], data[0]["lon"]
    towns = get_towns_in_radius(float(lat), float(lon), radius)
    return towns
