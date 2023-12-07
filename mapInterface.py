import folium
from geopy.geocoders import Nominatim
import webbrowser
import requests


def geocode_address(address):
    geolocator = Nominatim(user_agent="my_agent")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude if location else None


def draw_route(start_address, end_address):
    start_location = geocode_address(start_address)
    end_location = geocode_address(end_address)
    print(start_location, end_location)

    map_ = folium.Map(location=start_location, zoom_start=12)
    folium.Marker(location=start_location, popup='Start', tooltip=start_address).add_to(map_)
    folium.Marker(location=end_location, popup='End', tooltip=end_address).add_to(map_)

    # Get the route information using encoded polyline
    url = f"https://router.project-osrm.org/route/v1/driving/{start_location[1]},{start_location[0]};{end_location[1]},{end_location[0]}?overview=full&geometries=geojson"
    response = requests.get(url)

    if response.status_code == 200:
        route_data = response.json()
        route_geometry = route_data['routes'][0]['geometry']
        route = folium.features.GeoJson(route_geometry)
        map_.add_child(route)
    else:
        print("Error fetching route data.")

    map_.save('map_v1.html')



def drawAndShow(start, end):
    draw_route(start, end)
    webbrowser.open('map_v1.html')