from services.auth import AuthService


class AuthController:
    """Gère l'authentification des utilisateurs."""

    def __init__(self, session):
        self.auth_service = AuthService(session)

    def login(self, email, password):
        """Logs in a user"""
        return self.auth_service.login(email, password)

    def logout(self):
        """Logs out a user"""
        return self.auth_service.logout()

    def is_logged_in(self):
        """Check if a user in login and return his infos"""
        return self.auth_service.is_logged_in()
