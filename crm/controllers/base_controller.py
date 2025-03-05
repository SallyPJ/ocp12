from services.auth_service import AuthService
from services.permissions import PermissionService


class BaseController:
    """Contrôleur de base gérant l'authentification et la sécurité des contrôleurs enfants."""

    def __init__(self, session, dao_class):
        self.auth_service = AuthService(session)
        self.permission_service = PermissionService(session)
        self.user_id = None
        self.session = session  # ✅ On stocke la session

        if dao_class:  # ✅ Vérifie que `dao_class` est bien passé
            self.dao = dao_class(session)
        else:
            self.dao = None
            print(f"⚠️ Avertissement : Aucun `dao_class` défini pour {self.__class__.__name__}")

        # 🔹 Automatically retrieve access Token
