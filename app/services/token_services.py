import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")  # Use environment variables

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
