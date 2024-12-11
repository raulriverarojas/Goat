from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statsbomb import statsbomb_bp
from app import db
from statsbombpy import sb

@statsbomb_bp.route('/api', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(sb.competitions()), 200