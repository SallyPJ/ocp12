from dao.customer_dao import CustomerDAO
from dao.user_dao import UserDAO
from decorators.auth_decorators import require_auth, require_permission
from controllers.base_controller import BaseController
from views.customer_view import CustomerView


class CustomerController(BaseController):
    """Manage customers"""

    def __init__(self, session):
        super().__init__(session, CustomerDAO)
        self.user_dao = UserDAO(session)
        self.view = CustomerView()

    @require_auth
    @require_permission("read_all_clients")
    def list_customers(self):
        """Lists all customers"""
        customers = self.dao.get_all()
        if not customers:
            return self.view.no_customers_found()
        return self.view.display_customers(customers)

    @require_auth
    @require_permission("read_all_clients")
    def get_customer(self, customer_id):
        """Retrieves a specific customer"""
        customer = self.dao.get_by_id(customer_id)
        if not customer:
            return self.view.customer_not_found()
        return self.view.display_customer(customer)

    @require_auth
    @require_permission("create_clients")
    def create_customer(self, name, email, phone, enterprise):
        """Creates a new customer"""
        user = self.user_dao.get_by_id(self.user_id)

        # L'utilisateur est un admin (département 4) → pas de sales_contact
        # Sinon, il devient le sales_contact du client créé
        sales_contact = None if user.department_id == 4 else user.id

        # Passer `sales_contact` lors de la création du client
        new_customer = self.dao.create(name, email, phone, enterprise, sales_contact)
        return self.view.customer_created(new_customer)

    @require_auth
    @require_permission("edit_clients")
    def update_customer(self, customer_id, **kwargs):
        """Updates an existing customer if user is sales contact"""

        customer = self.dao.get_by_id(customer_id)
        if not customer:
            return self.view.customer_not_found()

        # Vérifier si l'utilisateur est autorisé à modifier ce client
        user = self.user_dao.get_by_id(self.user_id)
        if customer.sales_contact != self.user_id and user.department_id != 4:
            return self.view.access_denied()

        # Ne garder que les valeurs non nulles
        valid_updates = {k: v for k, v in kwargs.items() if v is not None}

        if not valid_updates:
            return self.view.no_changes_provided()

        # Générer un résumé des modifications
        summary = self.view.update_summary(valid_updates)

        # Demander confirmation via la vue
        if not self.view.confirm_update(summary):
            return self.view.update_cancelled()

        # Appliquer la mise à jour
        updated_customer = self.dao.update(customer_id, **valid_updates)
        return self.view.customer_updated(updated_customer)


