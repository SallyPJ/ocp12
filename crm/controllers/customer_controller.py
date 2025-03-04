from dao.customer_dao import CustomerDAO
from dao.user_dao import UserDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController


class CustomerController(BaseController):
    """Manage customers"""

    def __init__(self, session):
        super().__init__(session, CustomerDAO)
        self.user_dao = UserDAO(session)

    @require_permission("read_all_clients")
    def list_customers(self):
        """Lists all customers"""
        customers = self.dao.get_all()
        if not customers:
            return ["Aucun client trouvé."]
        return [f"{c.id} - {c.name} ({c.email})" for c in customers]

    @require_permission("read_all_clients")
    def get_customer(self, customer_id):
        """Retrieves a specific customer"""
        customer = self.dao.get_by_id(customer_id)
        if not customer:
            return "❌ Client non trouvé."
        return f"{customer.id} - {customer.name} ({customer.email})"

    @require_permission("create_clients")
    def create_customer(self, name, email, phone, enterprise):
        """Creates a new customer"""
        user = self.user_dao.get_by_id(self.user_id)
        self.dao.sales_contact = None if user.department_id == 4 else user.id

        new_customer = self.dao.create(name, email, phone, enterprise, self.user_id)
        return f"✅ Client {new_customer.name} ({new_customer.email}) ajouté avec succès."

    @require_permission("edit_clients")
    def update_customer(self, customer_id, **kwargs):
        """Updates an existing customer id user is sales contact"""
        customer = self.dao.get_by_id(customer_id)
        if not customer:
            return "❌ Client non trouvé."

        # check is user is sales_contact or admin
        if customer.sales_contact != self.user_id or self.user.department_id != 4:
            return "❌ Vous n'êtes pas responsable de ce client."

        updated_customer = self.dao.update(customer_id, **kwargs)
        return f"✅ Client {updated_customer.name} mis à jour avec succès."
