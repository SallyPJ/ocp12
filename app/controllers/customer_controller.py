from dao.customer_dao import CustomerDAO

class CustomerController:
    """Gère les clients en lecture seule."""

    def __init__(self, session):
        self.customer_dao = CustomerDAO(session)

    def list_customers(self):
        """Retourne la liste de tous les clients."""
        customers = self.customer_dao.get_all()
        if not customers:
            return ["Aucun client trouvé."]
        return [f"{c.id} - {c.name} ({c.email})" for c in customers]

    def get_customer(self, customer_id):
        """Retourne un client spécifique."""
        customer = self.customer_dao.get_by_id(customer_id)
        if not customer:
            return "❌ Client non trouvé."
        return f"{customer.id} - {customer.name} ({customer.email})"
