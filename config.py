import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    POSTMARK_SENDING_EMAIL = os.getenv('POSTMARK_SENDING_EMAIL') or 'your-sending-email@domain.com'
    POSTMARK_SERVER_TOKEN = os.getenv('POSTMARK_SERVER') or 'POSTMARK_API_TEST'
