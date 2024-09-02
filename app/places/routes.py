from flask import request, jsonify
from app.config import gmaps
from app.places import places_bp


# Endpoint for  Get Places according to type
@places_bp.route('/get-places', methods=['GET'])
def get_places():
    location_name = request.args.get('location_name')
    radius = int(request.args.get('radius', 5000))
    place_type = request.args.get('type')   

    if not location_name:
        return jsonify({"error": "Location name is required"}), 400

    lat, lon = get_lat_lon(location_name)

    if not lat or not lon:
        return jsonify({"error": "Could not find coordinates for the provided location"}), 400

    try:
        location = f"{lat},{lon}"
        places_result = gmaps.places_nearby(location=location, radius=radius, type=place_type)
        return jsonify(places_result), 200
    except Exception as e:
        return f"Failed to fetch places: {str(e)}", 500

# Function to Geocode location name to latitute and longitude, using Google cloud geocoding api
def get_lat_lon(location_name):
    geocode_result = gmaps.geocode(location_name)
    if not geocode_result:
        return None, None

    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    return lat, lon
