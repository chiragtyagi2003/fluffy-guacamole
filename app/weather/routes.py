from flask import request, jsonify
from app.weather import weather_bp
from app.places.routes import get_lat_lon
import requests
import os

# Endpoint for Source Weather
@weather_bp.route('/get-weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')

    if not location:
        return jsonify({"error": "Location name is required"}), 400

    lat, lon = get_lat_lon(location)

    if not lat or not lon:
        return jsonify({"error": "Could not find coordinates for the provided location"}), 400

    try:
        weather_api_key = os.getenv("WEATHER_API_KEY")
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code != 200:
            return jsonify({"error": weather_data.get("message", "Failed to fetch weather")}), weather_response.status_code

        return jsonify(weather_data), 200
    except Exception as e:
        return f"Failed to fetch weather: {str(e)}", 500

# New Endpoint for Destination Weather
@weather_bp.route('/get-destination-weather', methods=['GET'])
def get_destination_weather():
    location = request.args.get('location')

    if not location:
        return jsonify({"error": "Location name is required"}), 400

    lat, lon = get_lat_lon(location)

    if not lat or not lon:
        return jsonify({"error": "Could not find coordinates for the provided location"}), 400

    try:
        weather_api_key = os.getenv("WEATHER_API_KEY")
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code != 200:
            return jsonify({"error": weather_data.get("message", "Failed to fetch weather")}), weather_response.status_code

        return jsonify(weather_data), 200
    except Exception as e:
        return f"Failed to fetch weather: {str(e)}", 500
