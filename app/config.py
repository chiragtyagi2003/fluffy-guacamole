import os
import firebase_admin
from firebase_admin import credentials
import google.generativeai as genai
import googlemaps

# Initialize Firebase Admin SDK
cred = credentials.Certificate("atlan_firebase_creds.json")
firebase_admin.initialize_app(cred)


# Set up the Google Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Google Gemini model    
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Google Maps API client
gmaps = googlemaps.Client(key="AIzaSyBvQn2U-8RObBlrWbots9zKUwIbCf0Uneg")


