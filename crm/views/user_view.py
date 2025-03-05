class UserView:
    """Handles user messages and formatting for CLI output"""

    @staticmethod
    def display_users(users):
        return [
            {
                "ID": user.id,
                "Prénom": user.first_name,
                "Nom": user.last_name,
                "Email": user.email,
                "Département": user.department_id if user.department_id else "N/A",
                "Statut": user.active
            }
            for user in users
        ]

    @staticmethod
    def user_exists():
        return "❌ Un utilisateur avec cet email existe déjà."

    @staticmethod
    def user_created(user):
        return f"✅ Utilisateur {user.email} créé avec succès."

    @staticmethod
    def user_not_found():
        return "❌ Utilisateur non trouvé."

    @staticmethod
    def user_updated(user):
        return f"✅ Utilisateur {user.email} mis à jour avec succès."

    @staticmethod
    def user_deleted(user):
        return f"✅ Utilisateur {user.email} supprimé."

    @staticmethod
    def user_deactivated(user):
        return f"✅ L'utilisateur {user.email} a été désactivé."
