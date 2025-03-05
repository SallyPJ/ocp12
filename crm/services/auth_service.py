from passlib.hash import argon2
from dao.user_dao import UserDAO
from services.token_service import TokenService
from config import SECRET_KEY, REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN


class AuthService:
    """Manages secure user authentication."""

    def __init__(self, session):
        self.user_dao = UserDAO(session)

    def login(self, email, password):
        """Verifies user identity and logs them in.
        Checks if the provided credentials match a user in the database.
        If valid, generates and stores access and refresh tokens.
        """
        user = self.user_dao.get_by_email(email)
        if not user or not argon2.verify(password, user._password):
            return "❌ Identifiants incorrects."

        tokens = {
            "access_token": TokenService.generate_token(user, ACCESS_TOKEN_EXPIRES_IN, SECRET_KEY, "access"),
            "refresh_token": TokenService.generate_token(user, REFRESH_TOKEN_EXPIRES_IN, REFRESH_SECRET_KEY, "refresh"),
        }
        TokenService.write_session(tokens)

        return "✅ Connexion réussie !"

    def logout(self):
        """Logs out the user by clearing authentication tokens from the session."""
        TokenService.clear_session()
        return "✅ Déconnexion réussie."

    def refresh_token(self):
        """Renews the access token using the refresh token."""
        return TokenService.refresh_access_token()

    def is_logged_in(self, user_id):
        """Checks if a user is logged in and returns their information.
        Retrieves user details from the database using the provided user ID.
        """
        user = self.user_dao.get_by_id(user_id)  # ✅ Utilisation directe de self.user_id

        if user:
            return {
                "id": user.id,
                "email": user.email,
            }

        return None
