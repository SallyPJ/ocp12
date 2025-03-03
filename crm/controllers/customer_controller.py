from dao.customer_dao import CustomerDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController

class CustomerController(BaseController):
    """Gère les clients en lecture seule."""

    def __init__(self, session):
        super().__init__(session, CustomerDAO)

    @require_permission("read_all_clients")
    def list_customers(self):
        """Retourne la liste de tous les clients."""
        customers = self.customer_dao.get_all()
        if not customers:
            return ["Aucun client trouvé."]
        return [f"{c.id} - {c.name} ({c.email})" for c in customers]

    @require_permission("read_all_clients")
    def get_customer(self, customer_id):
        """Retourne un client spécifique."""
        customer = self.customer_dao.get_by_id(customer_id)
        if not customer:
            return "❌ Client non trouvé."
        return f"{customer.id} - {customer.name} ({customer.email})"

    @require_permission("create_clients")
    def create_customer(self, name, email, phone, enterprise):
        """Crée un nouveau client."""
        user_id = None if self.user.department_id == 4  else self.user_id

        new_customer = self.dao.create(name, email, phone, enterprise, self.user_id)
        return f"✅ Client {new_customer.name} ({new_customer.email}) ajouté avec succès."

    @require_permission("edit_clients")
    def update_customer(self, customer_id, **kwargs):
        """Met à jour un client si l'utilisateur est responsable."""
        customer = self.dao.get_by_id(customer_id)
        if not customer:
            return "❌ Client non trouvé."

        # Vérifie si l'utilisateur est le commercial responsable
        if customer.sales_contact != self.user_id or self.user.department_id != 4:
            return "❌ Vous n'êtes pas responsable de ce client."

        updated_customer = self.dao.update(customer_id, **kwargs)
        return f"✅ Client {updated_customer.name} mis à jour avec succès."