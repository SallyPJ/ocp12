from dao.user_dao import UserDAO


class PermissionService:
    """Manages user access permissions."""

    def __init__(self, session):
        self.user_dao = UserDAO(session)

    def has_permission(self, user_id, permission_name):
        """Checks if the user has a specific permission.

        Retrieves the user from the database and verifies if the given permission
        exists in the user's department permissions.

        Returns:
            bool: True if the user has the specified permission, False otherwise.
        """
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False

        user_permissions = {perm.name for perm in user.department.permissions}
        return permission_name in user_permissions



