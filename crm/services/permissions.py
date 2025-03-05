import functools
from dao.user_dao import UserDAO


class PermissionService:
    """Gère l'accès aux permissions des utilisateurs."""

    def __init__(self, session):
        self.user_dao = UserDAO(session)

    def has_permission(self, user_id, permission_name):
        """Vérifie si l'utilisateur possède une permission spécifique."""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False

        user_permissions = {perm.name for perm in user.department.permissions}
        return permission_name in user_permissions



