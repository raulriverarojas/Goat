import os
from datetime import timedelta
from dotenv import load_dotenv

result = load_dotenv()



class Config:
    VERIFICATION_TOKEN_KEY = os.getenv("VERIFICATION_TOKEN_KEY") or "your-secret-key"
    VERIFICATION_TOKEN_SALT = os.getenv("VERIFICATION_TOKEN_SALT") or "verification-salt"
    RESET_TOKEN_KEY = os.getenv("RESET_TOKEN_KEY") or "your-secret-key"
    RESET_TOKEN_SALT = os.getenv("RESET_TOKEN_SALT") or "verification-salt"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    POSTMARK_SENDING_EMAIL = os.getenv("POSTMARK_SENDING_EMAIL") or "your-sending-email@domain.com"
    POSTMARK_SERVER_TOKEN = os.getenv("POSTMARK_SERVER_TOKEN") or "POSTMARK_API_TEST"
    SUPPORT_EMAIL= os.getenv("SUPPORT_EMAIL") or "support@domain"
    FRONTEND = os.getenv("FRONTEND") or "http://localhost:3000"