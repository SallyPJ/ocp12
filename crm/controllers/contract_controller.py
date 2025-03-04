from dao.contract_dao import ContractDAO
from dao.customer_dao import CustomerDAO
from dao.user_dao import UserDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController


class ContractController(BaseController):
    """Manage contracts"""

    def __init__(self, session):
        super().__init__(session, ContractDAO)
        self.customer_dao = CustomerDAO(session)
        self.user_dao = UserDAO(session)

    @require_permission("read_all_contracts")
    def list_contracts(self, customer_id=None, is_signed=None, sales_contact=None, is_paid=None):
        """Lists contracts with optional filters"""
        contracts = self.dao.get_filtered_contracts(
            customer_id=customer_id, is_signed=is_signed, sales_contact=sales_contact, is_paid=is_paid
        )

        if not contracts:
            return []

        return [
            {
                "id": c.id,
                "customer_id": c.customer_id,
                "sales_contact": c.sales_contact,
                "total_amount": c.total_amount,
                "due_amount": c.due_amount,
                "creation_date": c.creation_date.strftime("%Y-%m-%d"),
                "is_signed": c.is_signed,
                "is_paid": c.due_amount == 0,
                "customer_name": c.customer.name if c.customer else "N/A",
                "sales_contact_name": (
                    f"{c.sales_contact_user.first_name} {c.sales_contact_user.last_name}"
                    if c.sales_contact_user
                    else "N/A"
                ),
            }
            for c in contracts
        ]

    @require_permission("read_all_contracts")
    def get_contract(self, contract_id):
        """Retrieves a specific contract"""
        contract = self.dao.get_by_id(contract_id)
        if not contract:
            return "❌ Contrat non trouvé."
        return contract

    @require_permission("create_contracts")
    def create_contract(self, customer_id, total_amount, due_amount, is_signed):
        """Creates a new contract"""
        try:
            sales_contact = self._get_sales_contact_for_customer(customer_id)
        except ValueError as e:
            return str(e)
        contract = self.dao.create_contract(customer_id, sales_contact, total_amount, due_amount, is_signed)
        return f"✅ Contrat {contract.id} créé avec succès."

    @require_permission("edit_contracts")
    def update_contract(self, contract_id, **kwargs):
        """Updates an existing contract"""
        contract = self.dao.get_by_id(contract_id)
        if not contract:
            return "❌ Contrat non trouvé."

        user = self.user_dao.get_by_id(self.user_id)
        if contract.sales_contact != user.id and user.department_id not in (1, 4):
            return "❌ Vous n'êtes pas responsable de ce contrat."

        # ✅ Si `customer_id` change, mettre à jour automatiquement `sales_contact`
        new_customer_id = kwargs.get("customer_id")
        if new_customer_id and new_customer_id != contract.customer_id:
            try:
                kwargs["sales_contact"] = self._get_sales_contact_for_customer(new_customer_id)
            except ValueError as e:
                return str(e)

        contract = self.dao.update_contract(contract_id, **kwargs)
        return f"✅ Contrat {contract.id} mis à jour avec succès."

    def _get_sales_contact_for_customer(self, customer_id):
        """Retrieves the sales contact for a customer"""
        customer = self.customer_dao.get_by_id(customer_id)

        if not customer:
            raise ValueError(f"❌ Client ID {customer_id} introuvable.")

        if not customer.sales_contact:
            raise ValueError(f"❌ Le client ID {customer_id} n'a pas de commercial assigné.")

        return customer.sales_contact
