from flask import Blueprint

itinerary_bp = Blueprint('itinerary', __name__)

from app.itinerary import routes
