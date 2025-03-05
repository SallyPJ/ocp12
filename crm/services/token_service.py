# 📌 services/token_service.py
import jwt
import json
import datetime
import keyring
from config import SECRET_KEY, REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN

ISSUER = "EpicEvents"

class TokenService:
    """Gère la génération, la validation et le stockage sécurisé des tokens JWT."""

    @staticmethod
    def generate_token(user, expires_in, secret_key, token_type):
        """Crée un JWT avec une durée de validité."""
        payload = {
            "user_id": user.id,
            "iss": ISSUER,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
            "type": token_type,
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")

    @staticmethod
    def decode_token(token, secret_key):
        """Décode un JWT et vérifie sa validité."""
        try:
            return jwt.decode(token, secret_key, algorithms=["HS256"], issuer=ISSUER)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def read_session():
        """Récupère les tokens stockés de manière sécurisée via Keyring."""
        data = keyring.get_password("EpicEvents", "session")
        return json.loads(data) if data else {}

    @staticmethod
    def write_session(session_data):
        """Sauvegarde sécurisée des tokens via Keyring."""
        keyring.set_password("EpicEvents", "session", json.dumps(session_data))

    @staticmethod
    def clear_session():
        """Supprime les tokens stockés."""
        keyring.delete_password("EpicEvents", "session")

    @staticmethod
    def refresh_access_token():
        """Génère un nouvel access_token en utilisant le refresh_token."""
        session_data = TokenService.read_session()
        refresh_token = session_data.get("refresh_token")

        if not refresh_token:
            return None  # Aucun refresh token stocké

        decoded = TokenService.decode_token(refresh_token, REFRESH_SECRET_KEY)
        if not decoded:
            return None  # Refresh token invalide ou expiré

        # Génération d'un nouveau token d'accès
        user_id = decoded["user_id"]
        new_access_token = TokenService.generate_token(
            type("User", (object,), {"id": user_id}),  # Simulation d'un user object
            ACCESS_TOKEN_EXPIRES_IN,
            SECRET_KEY,
            "access",
        )

        session_data["access_token"] = new_access_token
        TokenService.write_session(session_data)

        return new_access_token
