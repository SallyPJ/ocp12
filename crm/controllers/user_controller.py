from dao.user_dao import UserDAO
from models.user import User
from services.permissions import require_permission
from controllers.base_controller import BaseController


class UserController (BaseController):
    """Gère les actions utilisateur sans interagir directement avec la BD."""

    def __init__(self, session):
        super().__init__(session, UserDAO)

    @require_permission("create_employees")
    def create_user(self, first_name, last_name, email, password, department_id, active=True):
        """Créer un nouvel utilisateur avec vérifications métier."""
        if self.dao.exists(email):
            return "❌ Un utilisateur avec cet email existe déjà."

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department_id,
            password=password,
            active=active,
        )

        self.dao.save(new_user)
        return f"✅ Utilisateur {new_user.email} créé avec succès."

    @require_permission("edit_employees")
    def update_user(self, user_id, **kwargs):
        """Met à jour les informations d'un utilisateur existant."""
        user = self.dao.get_by_id(user_id)
        if not user:
            return "❌ Utilisateur non trouvé."

        self.dao.update(user, **kwargs)
        return f"✅ Utilisateur {user.email} mis à jour avec succès."

    @require_permission("delete_employees")
    def delete_user(self, user_id):
        """Supprime un utilisateur."""
        user = self.dao.get_by_id(user_id)
        if not user:
            return "❌ Utilisateur non trouvé."

        self.dao.delete(user)
        return f"✅ Utilisateur {user.email} supprimé."

    @require_permission("read_all_employees")
    def list_users(self):
        """Retourne la liste des utilisateurs sous forme de texte."""
        users = self.dao.get_all()
        if not users:
            return ["Aucun utilisateur trouvé."]
        return [f"{user.id} - {user.first_name} {user.last_name} ({user.email})" for user in users]

    @require_permission("edit_employees")
    def deactivate_user(self, user_id):
        """Désactive un utilisateur (par exemple lors de la démission)."""
        user = self.user_dao.get_by_id(user_id)
        if user:
            self.user_dao.deactivate_user(user_id)
            return f"✅ L'utilisateur {user.email} a été désactivé."
        return "❌ Utilisateur non trouvé."