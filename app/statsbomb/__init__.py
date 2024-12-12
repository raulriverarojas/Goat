from flask import Blueprint

statsbomb_bp = Blueprint("statsbomb", __name__)

from app.statsbomb import routes