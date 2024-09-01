from flask import Flask
from dotenv import load_dotenv
from app.auth.routes import auth_bp


def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
      
    # Import config.py to initialize Firebase and other services
    from app import config

    # Register blueprints
    app.register_blueprint(auth_bp)
    
    return app
