from services.auth_service import AuthService
from decorators.auth_decorators import require_auth, require_permission



class AuthController:
    """Gère l'authentification des utilisateurs."""

    def __init__(self, session):
        self.auth_service = AuthService(session)

    def login(self, email, password):
        """Logs in a user"""
        return self.auth_service.login(email, password)

    @require_auth
    def logout(self):
        """Logs out a user"""
        return self.auth_service.logout()

    @require_auth
    def is_logged_in(self, user_payload):
        """Check if a user in login and return his infos"""
        return self.auth_service.is_logged_in(user_payload["user_id"])
