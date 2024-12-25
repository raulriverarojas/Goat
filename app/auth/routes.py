from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.auth import auth_bp
from app.models import User
from app.signals import send_verification_code, send_reset_password
from app import verification_serializer, reset_serializer

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if "username" in data and "password" in data:
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"msg": "Username already exists"}), 409
        
        user = User(username=data["username"])
        if user.set_password(data["password"]):
            user.save()
            return jsonify({"msg": "User created successfully"}), 201
    return jsonify({"msg": "Invalid Credentials"}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    
    try:
        if user: 
            if not user.verified:
                return jsonify({"msg": "Please verify your account to be able to log in"}), 401
            if user.check_password(data["password"]):
                access_token = create_access_token(identity=user.get_username())
                set_access_cookies(response, access_token)
                return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"msg": "Invalid credentials"}), 401
    return jsonify({"msg": "Invalid credentials"}), 401

@auth_bp.route("/verify-email", methods=["POST"])
def validate_email():
    data = request.get_json()

    try:
        verified_username = verification_serializer.loads(data["token"], max_age=86400) 
        user = User.query.filter_by(username=verified_username, verified=False).first()
        if user:
            user.verify_user()
            return jsonify({"msg": "User validated"}), 200 
        return jsonify({"msg": "No unverified user exists for this token"}), 400
    except Exception as e:
        return jsonify({"msg": "Invalid Token" }), 400

@auth_bp.route("/request-email-verification-code", methods=["POST"])
def request_email_verification_code():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"], verified=False).first()
    if user:
        send_verification_code.send(user)
    return jsonify({"msg": "If a user exists with this username, an email will be sent to this email"}), 200

@auth_bp.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"], verified=True).first()
    send_reset_password.send(user)
    return jsonify({"msg": "If a user exists with this username, an email will be sent to this email"}), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    try:
        username, token2 = reset_serializer.loads(data["token"], max_age=3600) 
        
        user = User.query.filter_by(username=username, verified=True).first()
        if reset_serializer.loads(token2, max_age=3600, salt=user.get_password_hash()):
            user.set_password(data["password"])
            user.save()
            return jsonify({"msg": "Password changed"}), 200 
        return jsonify({"msg": "Invalid Token"}), 400
    except Exception as e:
        return jsonify({"msg": "Invalid Token" }), 400