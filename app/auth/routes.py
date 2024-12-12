from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.auth import auth_bp
from app.models import User
from app.signals import user_created
from app import dangerous_serializer

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 409
    
    user = User(username=data['username'])
    if user.set_password(data['password']):
        user.save()
        return jsonify({"msg": "User created successfully"}), 201
    return jsonify({"msg": "Invalid password"}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token}), 200
    
    return jsonify({"msg": "Invalid credentials"}), 401
@auth_bp.route('/validate', methods=['POST'])
def validate_email():
    data = request.get_json()

    try:
        verified_username = dangerous_serializer.loads(data['token'], max_age=86400) 
        user = User.query.filter_by(username=verified_username, verified=False).first()
        if user:
            user.verify_user()
            return jsonify({"msg": "User validated"}), 200 
        return jsonify({"msg": "No unverified user exists for this token"}), 400
    except Exception as e:
        return jsonify({"msg": "Invalid Token" }), 400