from dao.user_dao import UserDAO
from models.user import User

class UserController:
    """Gère les actions utilisateur sans interagir directement avec la BD."""

    def __init__(self, session):
        self.user_dao = UserDAO(session)

    def create_user(self, first_name, last_name, email, password, department_id):
        """Créer un nouvel utilisateur avec vérifications métier."""
        if self.user_dao.exists(email):
            return "❌ Un utilisateur avec cet email existe déjà."

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department_id,
            password=password
        )

        self.user_dao.save(new_user)
        return f"✅ Utilisateur {new_user.email} créé avec succès."

    def update_user(self, user_id, **kwargs):
        """Met à jour les informations d'un utilisateur existant."""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return "❌ Utilisateur non trouvé."

        self.user_dao.update(user, **kwargs)
        return f"✅ Utilisateur {user.email} mis à jour avec succès."

    def delete_user(self, user_id):
        """Supprime un utilisateur."""
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return "❌ Utilisateur non trouvé."

        self.user_dao.delete(user)
        return f"✅ Utilisateur {user.email} supprimé."

    def list_users(self):
        """Retourne la liste des utilisateurs sous forme de texte."""
        users = self.user_dao.get_all()
        if not users:
            return ["Aucun utilisateur trouvé."]
        return [f"{user.id} - {user.first_name} {user.last_name} ({user.email})" for user in users]