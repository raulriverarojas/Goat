from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statsbomb import statsbomb_bp
from app import db
from statsbombpy import sb

@statsbomb_bp.route("/competitions", methods=["GET"])
@jwt_required()
def get_competitions():
    current_user = get_jwt_identity()
    dataframe = sb.competitions(fmt="dict")
    filter_competitions = lambda d: {k: v for k, v in d.items() if v.get('competition_id') in [16, 223, 87, 11]}
    filtered_competitions = filter_competitions(dataframe)
    return jsonify(filtered_competitions), 200