from flask import request, jsonify
from app.config import model
from app.itinerary import itinerary_bp
import json

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

