# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import Config
from argon2 import PasswordHasher

db = SQLAlchemy()
jwt = JWTManager()
ph = PasswordHasher()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    app.ph = ph
    
    from app.commands import init_db_command, seed_db_command
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    
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
