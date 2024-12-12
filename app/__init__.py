# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import Config
from argon2 import PasswordHasher
from dotenv import load_dotenv
from itsdangerous.url_safe import URLSafeTimedSerializer
from postmarker.core import PostmarkClient
import hashlib

db = SQLAlchemy()
jwt = JWTManager()
ph = PasswordHasher()
dangerous_serializer = URLSafeTimedSerializer(Config.VERIFICATION_TOKEN_KEY, Config.VERIFICATION_TOKEN_SALT, signer_kwargs={"digest_method": hashlib.sha512})
postmark = PostmarkClient(server_token=Config.POSTMARK_SERVER_TOKEN)
 


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    app.ph = ph
    app.dangerous_serializer = dangerous_serializer
    app.postmark = postmark
    
    from app.commands import init_db_command, seed_db_command
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.statsbomb import statsbomb_bp
    app.register_blueprint(statsbomb_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()

    @app.shell_context_processor
    def make_shell_context():
        # Import models here to avoid circular imports
        from app.models import User
        return {
            'db': db,
            'User': User,
            # Add other models or objects you want available in shell
        }

    return app
