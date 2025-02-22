import jwt as pyjwt
import datetime
import os
from sqlalchemy.orm import Session
from passlib.hash import argon2
from models import User
from services.constants import DEPARTMENTS
from config import SECRET_KEY, REFRESH_SECRET



def authenticate_user(session: Session, email: str, password: str):
    """Verifies user credentials and returns both an access and refresh token."""
    user = session.query(User).filter_by(email=email).first()

    if not user or not argon2.verify(password, user.password):
        print("❌ Invalid credentials")
        return None, None

    # ✅ Generate Access Token (Expires in 1 hour)
    access_payload = {
        "user_id": user.id,
        "email": user.email,
        "department": user.department.name,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1-hour expiration
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")

    # ✅ Generate Refresh Token (Expires in 7 days)
    refresh_payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 7-day expiration
    }
    refresh_token = jwt.encode(refresh_payload, REFRESH_SECRET, algorithm="HS256")

    print("✅ Authentication successful")
    return access_token, refresh_token

def check_permission(session: Session, user_email: str, required_permission: str):
    """Checks if a user has the required permission."""
    user = session.query(User).filter_by(email=user_email).first()
    if not user:
        return False

    department_permissions = DEPARTMENTS[user.department.name]["permissions"]
    return required_permission in department_permissions