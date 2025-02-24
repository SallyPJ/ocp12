import jwt
import json
import datetime
import functools
from config import SECRET_KEY, REFRESH_SECRET

def save_tokens(access_token, refresh_token):
    with open(".auth_token", "w") as f:
        json.dump({"access_token": access_token, "refresh_token": refresh_token}, f)

def load_tokens():
    """Charge les tokens depuis le fichier."""
    try:
        with open(".auth_token", "r") as f:
            tokens = json.load(f)
        return tokens.get("access_token"), tokens.get("refresh_token")
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

def verify_token(token):
    """Vérifie la validité d’un token JWT."""
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
    """Génère un nouveau token d’accès à partir du refresh token."""
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
        new_access_payload = {
            "user_id": payload["user_id"],
            "email": payload["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
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
    """Décorateur qui vérifie la validité du token avant d'exécuter une fonction.
    Il n’ouvre pas de transaction, la session doit être gérée par l’appelant."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        access_token, refresh_token = load_tokens()
        if not access_token or not refresh_token:
            print("❌ No tokens found. Please login first.")
            return None
        payload = verify_token(access_token)
        if payload is None:
            access_token = refresh_access_token(refresh_token)
            if access_token:
                save_tokens(access_token, refresh_token)
                payload = verify_token(access_token)
            else:
                print("❌ Refresh token expired. Please login again.")
                return None
        # On peut injecter des infos utilisateur dans kwargs si besoin
        kwargs["user_payload"] = payload
        return func(*args, **kwargs)
    return wrapper