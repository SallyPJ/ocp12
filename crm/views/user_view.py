class UserView:
    """Handles user messages and formatting for CLI output"""

    @staticmethod
    def format_user(user):
        """Format a single user for display"""
        return (
            f"👤 ID: {user.id} - {user.first_name} {user.last_name}\n"
            f"📧 Email: {user.email}\n"
            f"🏢 Département: {user.department.name if user.department else 'Non assigné'}\n"
            f"🔐 Statut: {'Actif' if user.active else 'Inactif'}\n"
        )

    @staticmethod
    def user_exists():
        return "❌ Un utilisateur avec cet email existe déjà."

    @staticmethod
    def user_created(user):
        return f"✅ Utilisateur {user.email} (ID: {user.id}) créé avec succès."

    @staticmethod
    def user_not_found():
        return "❌ Utilisateur non trouvé."

    @staticmethod
    def user_updated(user):
        return f"✅ Utilisateur {user.email} (ID: {user.id}) mis à jour avec succès."

    @staticmethod
    def user_deleted(user):
        return f"✅ Utilisateur {user.email} supprimé."

    @staticmethod
    def user_deactivated(user):
        return f"✅ L'utilisateur {user.email} a été désactivé."
