import jwt
import os
import functools
from config import SECRET_KEY, REFRESH_SECRET

def save_token(token):
    """Stores the token in a local file securely."""
    with open(".auth_token", "w") as f:
        f.write(token)

def load_token():
    """Loads the stored token."""
    try:
        with open(".auth_token", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def verify_token(token):
    """Verifies the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("❌ Token expired. Please login again.")
        return None
    except jwt.InvalidTokenError:
        print("❌ Invalid token.")
        return None


def refresh_access_token(refresh_token):
    """Uses the refresh token to generate a new access token."""
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])

        # ✅ Generate a new access token
        new_access_payload = {
            "user_id": payload["user_id"],
            "email": payload["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # New 1-hour expiration
        }
        new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm="HS256")

        print("✅ Access token refreshed automatically!")
        return new_access_token
    except jwt.ExpiredSignatureError:
        print("❌ Refresh token expired. Please login again.")
        return None
    except jwt.InvalidTokenError:
        print("❌ Invalid refresh token.")
        return None

def require_auth(func):
    """Decorator to check and refresh JWT tokens before executing any protected function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        access_token, refresh_token = load_tokens()

        if not access_token or not refresh_token:
            print("❌ No tokens found. Please login first.")
            return None  # User needs to reauthenticate

        # ✅ Verify the access token
        payload = verify_token(access_token)

        if payload is None:  # Token is expired, try to refresh
            access_token = refresh_access_token(refresh_token)
            if access_token:
                save_tokens(access_token, refresh_token)  # ✅ Save new access token
            else:
                print("❌ Refresh token expired. Please login again.")
                return None  # User needs to reauthenticate

        # ✅ If we reach here, the token is valid, proceed with the function
        return func(*args, **kwargs)

    return wrapper