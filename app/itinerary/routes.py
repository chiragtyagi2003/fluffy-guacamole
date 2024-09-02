from flask import request, jsonify, current_app
from app.config import model
from app.itinerary import itinerary_bp
import json
from datetime import datetime

# Existing Itinerary API
@itinerary_bp.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    data = request.get_json()
    if not data:
        return "Bad request", 400

    budget = data.get('budget')
    interests = data.get('interests', [])
    duration = data.get('duration')
    source = data.get('source')

    prompt = create_prompt(source, budget, interests, duration)

    try:
        response = call_gemini_api(prompt)
        return jsonify({"itinerary": response})
    except Exception as e:
        return f"Failed to generate itinerary: {str(e)}", 500


# function to create prompt for gemini api to generate itineray with source only in the defined json format
def create_prompt(source, budget, interests, duration):
    return (
        f"Generate a travel itinerary starting from {source} "
        f"with a budget of {budget} rupees, focusing on the following interests: {interests}, "
        f"for a duration of {duration} days. Return the response in JSON format only, ensuring it always follows this structure:\n\n"
        "{\n"
        "  \"budget\": {\n"
        "    \"breakdown\": {\n"
        "      \"accommodation\": \"string\",\n"
        "      \"activities\": \"string\",\n"
        "      \"food\": \"string\",\n"
        "      \"miscellaneous\": \"string\",\n"
        "      \"transportation\": \"string\"\n"
        "    },\n"
        "    \"total\": \"string\"\n"
        "  },\n"
        "  \"places\": \"comma-separated list of all places included in the itinerary\",\n"
        "  \"itinerary\": {\n"
        "    \"days\": [\n"
        "      {\n"
        "        \"day\": number,\n"
        "        \"heading\": \"string\",\n"
        "        \"description\": \"string\",\n"
        "        \"activities\": [\n"
        "          {\n"
        "            \"name\": \"string\",\n"
        "            \"type\": \"string\",\n"
        "            \"cost\": \"string\"\n"
        "          }\n"
        "        ]\n"
        "      }\n"
        "    ]\n"
        "  },\n"
        "  \"notes\": \"string\"\n"
        "}"
    )
    
# function to call gemini api
def call_gemini_api(prompt):
    response = model.generate_content(prompt)
    response_text = response.text

    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    try:
        itinerary_json = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse JSON response") from e

    return itinerary_json


# New Itinerary API with Source and Destination
@itinerary_bp.route('/generate-itinerary-with-destination', methods=['POST'])
def generate_itinerary_with_destination():
    data = request.get_json()
    if not data:
        return "Bad request", 400

    # Extract user input
    budget = data.get('budget')
    interests = data.get('interests', [])
    duration = data.get('duration')
    source = data.get('source')
    destination = data.get('destination')

    # Create prompt for the Gemini API
    prompt = create_prompt_with_destination(source, destination, budget, interests, duration)

    try:
        # Call the Google Gemini API
        response = call_gemini_api(prompt)
        return jsonify({"itinerary": response})
    except Exception as e:
        return f"Failed to generate itinerary: {str(e)}", 500


# function to create prompt for gemini api to generate itineray with destination in the defined json format
def create_prompt_with_destination(source, destination, budget, interests, duration):
    return (
        f"Generate a travel itinerary starting from {source} to {destination} "
        f"with a budget of {budget} rupees, focusing on the following interests: {interests}, "
        f"for a duration of {duration} days. Return the response in JSON format only, ensuring it always follows this structure:\n\n"
        "{\n"
        "  \"budget\": {\n"
        "    \"breakdown\": {\n"
        "      \"accommodation\": \"string\",\n"
        "      \"activities\": \"string\",\n"
        "      \"food\": \"string\",\n"
        "      \"miscellaneous\": \"string\",\n"
        "      \"transportation\": \"string\"\n"
        "    },\n"
        "    \"total\": \"string\"\n"
        "  },\n"
        "  \"places\": \"comma-separated list of all places included in the itinerary\",\n"  # New field for places
        "  \"itinerary\": {\n"
        "    \"days\": [\n"
        "      {\n"
        "        \"day\": number,\n"
        "        \"heading\": \"string\",\n"
        "        \"description\": \"string\",\n"
        "        \"activities\": [\n"
        "          {\n"
        "            \"name\": \"string\",\n"
        "            \"type\": \"string\",\n"
        "            \"cost\": \"string\"\n"
        "          }\n"
        "        ]\n"
        "      }\n"
        "    ]\n"
        "  },\n"
        "  \"notes\": \"string\"\n"
        "}"
    )


# Endpoint for Saving user generated itineraries to mongo DB
@itinerary_bp.route('/save-itinerary', methods=['POST'])
def save_itinerary():
    try:
        db = current_app.config['db']
        users_collection = db['users']
        
        # Get the itinerary data from the request
        data = request.get_json()

        if not data or not data.get('user_email'):
            return jsonify({"error": "No data or email provided"}), 400

        user_email = data['user_email']

        # Add a created_at timestamp to the itinerary
        itinerary = {
            "created_at": datetime.now(),
            "itinerary_data": data['itinerary_data']  # Assuming `itinerary_data` contains the itinerary details
        }

        # Find the user by email and update their document by pushing the new itinerary into the itineraries array
        result = users_collection.update_one(
            {"email": user_email},
            {"$push": {"itineraries": itinerary}}
        )

        if result.matched_count > 0:
            return jsonify({"message": "Itinerary saved successfully!"}), 201
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Endpoint for Fetching saved itineraries from mongo DB
@itinerary_bp.route('/fetch-itineraries', methods=['GET'])
def fetch_itineraries():
    try:
        db = current_app.config['db']
        users_collection = db['users']
        
        # Get the user's email from the query parameters
        email = request.args.get('email')

        if not email:
            return jsonify({"error": "Email parameter is required"}), 400

        # Fetch the user document with the matching email
        user = users_collection.find_one({"email": email}, {'_id': 0, 'itineraries': 1})

        if user and 'itineraries' in user:
            return jsonify({"itineraries": user['itineraries']}), 200
        else:
            return jsonify({"message": "No itineraries found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
