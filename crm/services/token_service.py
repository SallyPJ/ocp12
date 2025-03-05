import jwt
import json
import datetime
import keyring
from config import SECRET_KEY, REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN

ISSUER = "EpicEvents"

class TokenService:
    """Manages JWT token generation, validation, and secure storage."""

    @staticmethod
    def generate_token(user, expires_in, secret_key, token_type):
        """Creates a JWT token with an expiration time.

        Args:
            user: The user object (or equivalent) containing the user ID.
            expires_in: Expiration time in seconds.
            secret_key: The secret key used to sign the token.
            token_type: The type of token (access or refresh).

        Returns:
            str: Encoded JWT token.
        """
        payload = {
            "user_id": user.id,
            "iss": ISSUER,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
            "type": token_type,
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")

    @staticmethod
    def decode_token(token, secret_key):
        """Decodes a JWT token and verifies its validity.

        Args:
            token: The encoded JWT token.
            secret_key: The secret key used to decode and verify the token.

        Returns:
            dict: Decoded token payload if valid.
            None: If the token is expired or invalid.
        """
        try:
            return jwt.decode(token, secret_key, algorithms=["HS256"], issuer=ISSUER)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def read_session():
        """Retrieves securely stored tokens from Keyring.
        Returns:
            dict: A dictionary containing stored session tokens.
        """
        data = keyring.get_password("EpicEvents", "session")
        return json.loads(data) if data else {}

    @staticmethod
    def write_session(session_data):
        """Securely saves tokens using Keyring.
        Args:
            session_data: Dictionary containing access and refresh tokens.
        """
        keyring.set_password("EpicEvents", "session", json.dumps(session_data))

    @staticmethod
    def clear_session():
        """Deletes stored tokens from Keyring."""
        keyring.delete_password("EpicEvents", "session")

    @staticmethod
    def refresh_access_token():
        """Generates a new access token using the refresh token.
        Returns:
            str: New access token if refresh is successful.
            None: If no valid refresh token is available.
        """
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
