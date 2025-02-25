from services.auth import AuthService

class AuthController:
    """Gère l'authentification des utilisateurs."""

    def __init__(self, session):
        self.auth_service = AuthService(session)

    def login(self, email, password):
        """Connecte un utilisateur."""
        return self.auth_service.login(email, password)

    def logout(self):
        """Déconnecte un utilisateur."""
        return self.auth_service.logout()