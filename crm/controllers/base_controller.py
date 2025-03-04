from services.auth import AuthService
from services.permissions import PermissionService


class BaseController:
    """Contrôleur de base gérant l'authentification et la sécurité des contrôleurs enfants."""

    def __init__(self, session, dao_class):
        self.auth_service = AuthService(session)
        self.permission_service = PermissionService(session)
        self.user_id = None
        self.dao = None

        # 🔹 Automatically retrieve access Token
        access_token = self.auth_service.get_valid_access_token()
        if not access_token:
            print("🔴 Aucun utilisateur connecté ou token invalide.")
            self.user_id = None  # ❌ Pas d'utilisateur authentifié
            self.dao = None
            return

        # 🔹 Check authentication via `AuthService`
        decoded_token = self.auth_service.decode_access_token(access_token)
        if not decoded_token:
            print("🔴 Accès refusé. Token invalide ou expiré.")
            self.user_id = None
            self.dao = None
            return

        self.user_id = decoded_token.get("user_id")

        # 🔹 Dynamique creation of DAO
        self.dao = dao_class(session)
