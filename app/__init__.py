from flask import Flask
from dotenv import load_dotenv  
from flask_cors import CORS
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Load environment variables
    load_dotenv()

    # Get the MongoDB connection string from the environment variables
    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')

    # Initialize the MongoDB client
    client = MongoClient(MONGODB_URI)

    # Connect to the specified database
    db = client[DATABASE_NAME]

    # Store the database instance in the app config
    app.config['db'] = db

    # Import config.py to initialize Firebase and other services
    from app import config

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.itinerary.routes import itinerary_bp
    from app.places.routes import places_bp
    from app.transportation.routes import transportation_bp
    from app.weather.routes import weather_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(itinerary_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(transportation_bp)
    app.register_blueprint(weather_bp)

    return app
