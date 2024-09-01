from flask import Blueprint

transportation_bp = Blueprint('transportation', __name__)

from app.transportation import routes
