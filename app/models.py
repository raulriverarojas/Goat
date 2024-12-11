from app import db
from app import ph
from app.passwordHelpers import PasswordHelpers

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def set_password(self, password):
        if PasswordHelpers.is_valid_password(password):
            self.password_hash = ph.hash(password)
            return True
        return False
    
    def check_password(self, password):
        return ph.verify(self.password_hash, password)