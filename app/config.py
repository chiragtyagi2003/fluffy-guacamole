import os
import firebase_admin
from firebase_admin import credentials
import googlemaps
import google.generativeai as genai

# Initialize Firebase Admin SDK
cred = credentials.Certificate("atlan_firebase_creds.json")
firebase_admin.initialize_app(cred)

# Initialize Google Maps API client
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

# Set up the Google Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Google Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')
