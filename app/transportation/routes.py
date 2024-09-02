from flask import request, jsonify
from app.config import gmaps
from app.transportation import transportation_bp
from app.places.routes import get_lat_lon  # Reusing the get_lat_lon function


# Endpoint for Get Directions
@transportation_bp.route('/get-transportation', methods=['GET'])
def get_transportation():
    origin_name = request.args.get('origin_name')  # Origin location name, e.g., 'New Delhi'
    destination_name = request.args.get('destination_name')  # Destination location name, e.g., 'Noida'

    if not origin_name or not destination_name:
        return jsonify({"error": "Origin and Destination names are required"}), 400

    # Convert origin and destination names to latitude and longitude
    origin_lat, origin_lon = get_lat_lon(origin_name)
    destination_lat, destination_lon = get_lat_lon(destination_name)

    if not origin_lat or not origin_lon or not destination_lat or not destination_lon:
        return jsonify({"error": "Could not find coordinates for the provided locations"}), 400

    try:
        modes = ['driving', 'walking', 'bicycling', 'transit']
        all_directions = {}

        # Format the origin and destination for the directions function
        origin = f"{origin_lat},{origin_lon}"
        destination = f"{destination_lat},{destination_lon}"

        for mode in modes:
            directions_result = gmaps.directions(origin, destination, mode=mode)
            all_directions[mode] = directions_result

        return jsonify(all_directions), 200
    except Exception as e:
        return f"Failed to fetch transportation details: {str(e)}", 500


# Function to Geocode location name to latitute and longitude, using Google cloud geocoding api
def get_lat_lon(location_name):
    geocode_result = gmaps.geocode(location_name)
    if not geocode_result:
        return None, None

    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    return lat, lon
