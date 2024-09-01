from flask import Blueprint

places_bp = Blueprint('places', __name__)

from app.places import routes
