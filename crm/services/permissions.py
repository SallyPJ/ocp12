import functools
from services.auth import AuthService
from dao.user_dao import UserDAO


class PermissionService:
    """Gère l'accès aux permissions des utilisateurs."""

    def __init__(self, session):
        self.user_dao = UserDAO(session)
        self.auth_service = AuthService(session)

    def has_permission(self, user_id, permission_name):
        """Vérifie si l'utilisateur possède une permission spécifique."""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False

        user_permissions = {perm.name for perm in user.department.permissions}
        return permission_name in user_permissions


def require_permission(permission_name):
    """Décorateur pour sécuriser les contrôleurs et éviter la redondance."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "user_id") or self.user_id is None:
                print("🔴 Action refusée : Vous devez être connecté pour effectuer cette action.")
                return

            if not self.permission_service.has_permission(self.user_id, permission_name):
                return ["❌ Permission refusée."]

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
