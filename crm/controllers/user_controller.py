from dao.user_dao import UserDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController


class UserController(BaseController):
    """Manage user's actions without interaction with DB"""

    def __init__(self, session):
        super().__init__(session, UserDAO)

    @require_permission("read_all_employees")
    def list_users(self):
        """Lists all users"""
        users = self.dao.get_all()
        if not users:
            return ["Aucun utilisateur trouvé."]
        return [f"{user.id} - {user.first_name} {user.last_name} ({user.email})" for user in users]

    @require_permission("create_employees")
    def create_user(self, first_name, last_name, email, password, department_id, active=True):
        """Creates a new user with business rules"""
        if self.dao.exists(email):
            raise ValueError("❌ Un utilisateur avec cet email existe déjà.")

        return self.dao.create(first_name, last_name, email, password, department_id, active)

    @require_permission("edit_employees")
    def update_user(self, user_id, **kwargs):
        """Updates an existing user's information"""
        user = self.dao.get_by_id(user_id)
        if not user:
            return "❌ Utilisateur non trouvé."
        updates = {k: v for k, v in kwargs.items() if v is not None}

        self.dao.update(user, **updates)
        return user

    @require_permission("delete_employees")
    def delete_user(self, user_id):
        """Deletes a user"""
        user = self.dao.get_by_id(user_id)
        if not user:
            return "❌ Utilisateur non trouvé."

        self.dao.delete(user)
        return f"✅ Utilisateur {user.email} supprimé."

    @require_permission("edit_employees")
    def deactivate_user(self, user_id):
        """Deactivates a user"""
        user = self.user_dao.get_by_id(user_id)
        if user:
            self.user_dao.deactivate_user(user_id)
            return f"✅ L'utilisateur {user.email} a été désactivé."
        return "❌ Utilisateur non trouvé."
