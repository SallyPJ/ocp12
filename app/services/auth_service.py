import jwt as pyjwt
import datetime
import os
from sqlalchemy.orm import Session
from passlib.hash import argon2
from models import User
from services.constants import DEPARTMENTS

# ✅ Secret key (DO NOT HARD-CODE IT, use environment variables instead)
SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")  # Replace in production

def authenticate_user(session: Session, email: str, password: str):
    """Verifies user credentials and returns a JWT token if successful."""
    user = session.query(User).filter_by(email=email).first()
    if not user or not argon2.verify(password, user.password):
        print("❌ Invalid credentials")
        return None

    # ✅ Generate JWT token
    payload = {
        "user_id": user.id,
        "email": user.email,
        "department": user.department.name,  # Get user's department
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expiration (1 hour)
    }
    token = pyjwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print("✅ Authentication successful")
    return token

def check_permission(session: Session, user_email: str, required_permission: str):
    """Checks if a user has the required permission."""
    user = session.query(User).filter_by(email=user_email).first()
    if not user:
        return False

    department_permissions = DEPARTMENTS[user.department.name]["permissions"]
    return required_permission in department_permissions