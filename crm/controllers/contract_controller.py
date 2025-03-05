from dao.contract_dao import ContractDAO
from dao.customer_dao import CustomerDAO
from dao.user_dao import UserDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController
from views.contract_view import ContractView


class ContractController(BaseController):
    """Manage contracts"""

    def __init__(self, session):
        super().__init__(session, ContractDAO)
        self.customer_dao = CustomerDAO(session)
        self.user_dao = UserDAO(session)
        self.view = ContractView()

    @require_permission("read_all_contracts")
    def list_contracts(self, **filters):
        """Lists contracts with optional filters"""
        contracts = self.dao.get_filtered_contracts(**filters)
        if not contracts:
            return self.view.no_contracts_found()
        return self.view.format_contracts(contracts)

    @require_permission("read_all_contracts")
    def get_contract(self, contract_id):
        """Retrieves a specific contract"""
        contract = self.dao.get_by_id(contract_id)
        if not contract:
            return self.view.contract_not_found()
        return self.view.format_contracts(contract)

    @require_permission("create_contracts")
    def create_contract(self, customer_id, total_amount, due_amount, is_signed):
        """Creates a new contract"""
        try:
            sales_contact = self._get_sales_contact_for_customer(customer_id)
        except ValueError as e:
            return self.view.error_message(str(e))

        contract = self.dao.create_contract(customer_id, sales_contact, total_amount, due_amount, is_signed)
        return self.view.contract_created(contract)

    @require_permission("edit_contracts")
    def update_contract(self, contract_id, **kwargs):
        """Updates an existing contract"""
        contract = self.dao.get_by_id(contract_id)
        if not contract:
            return self.view.contract_not_found()

        user = self.user_dao.get_by_id(self.user_id)
        if contract.sales_contact != user.id and user.department_id not in (1, 4):
            return self.view.access_denied()

        updated_contract = self.dao.update_contract(contract_id, **kwargs)
        return self.view.contract_updated(updated_contract)

    def _get_sales_contact_for_customer(self, customer_id):
        """Retrieves the sales contact for a customer"""
        customer = self.customer_dao.get_by_id(customer_id)

        if not customer:
            raise ValueError(f"❌ Client ID {customer_id} introuvable.")

        if not customer.sales_contact:
            raise ValueError(f"❌ Le client ID {customer_id} n'a pas de commercial assigné.")

        return customer.sales_contact

