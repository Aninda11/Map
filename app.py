from flask import Flask, render_template, request, jsonify
import folium
from geopy.geocoders import Photon
import certifi
import ssl
import geopy

app = Flask(__name__)

@app.route('/')
def index():
    # Create the map object centered on London
    map_obj = create_map()
    map_html = map_obj._repr_html_()
    return render_template('index.html', map=map_html)

def create_map():
    """Initialize and return a folium map centered on London."""
    latitude = 51.5074
    longitude = -0.1278
    map_obj = folium.Map(location=[latitude, longitude], zoom_start=16, tiles='OpenStreetMap')
    return map_obj

@app.route('/search', methods=['POST'])
def search():
    # Get coordinates from the request
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']

    # Perform a reverse geocoding to get location information
    location_info = perform_reverse_geocoding(latitude, longitude)

    return jsonify(location_info)

def perform_reverse_geocoding(lat, lon):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Photon(user_agent="geoapiExercises")
    location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)

    if location:
        return location.address
    else:
        return "No location found."

if __name__ == '__main__':
    app.run(debug=True)
