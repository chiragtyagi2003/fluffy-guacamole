from flask import Flask
from dotenv import load_dotenv
from app.auth.routes import auth_bp
from app.itinerary.routes import itinerary_bp
from app.places.routes import places_bp
from app.transportation.routes import transportation_bp


def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
      
    # Import config.py to initialize Firebase and other services
    from app import config

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(itinerary_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(transportation_bp)

    
    return app
