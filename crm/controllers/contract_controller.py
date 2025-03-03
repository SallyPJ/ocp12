from dao.contract_dao import ContractDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController
class ContractController(BaseController):
    """Gère les contrats en lecture seule."""

    def __init__(self, session):
        super().__init__(session, ContractDAO)

    @require_permission("read_all_contracts")
    def list_contracts(self, customer_id=None, is_signed=None, start_date=None, end_date=None, sales_contact=None, is_paid=None):
        """Retourne la liste des contrats, avec des filtres optionnels."""
        contracts = self.contract_dao.get_filtered_contracts(
            customer_id=customer_id,
            is_signed=is_signed,
            start_date=start_date,
            end_date=end_date,
            sales_contact=sales_contact,
            is_paid = is_paid
        )

        if not contracts:
            return ["Aucun contrat trouvé."]

        return [
            f"{c.id} - Client ID: {c.customer_id}, Montant: {c.total_amount}€, "
            f"Signé: {'✅ Oui' if c.is_signed else '❌ Non'}, Créé le: {c.creation_date.strftime('%Y-%m-%d')}"
            f"Payé: {'✅ Oui' if c.is_paid else '❌ Non'}, "
            f"Créé le: {c.creation_date.strftime('%Y-%m-%d')}"
            for c in contracts
        ]

    @require_permission("read_all_contracts")
    def get_contract(self, contract_id):
        """Retourne un contrat spécifique."""
        contract = self.contract_dao.get_by_id(contract_id)
        if not contract:
            return "❌ Contrat non trouvé."
        return (f"Contrat {contract.id} - Client ID: {contract.customer_id}, Montant: {contract.total_amount}€,"
                f"Signé: {'✅ Oui' if contract.is_signed else '❌ Non'}")

    @require_permission("create_contracts")
    def create_contract(self, customer_id, sales_contact, total_amount, due_amount, is_signed):
        """Crée un nouveau contrat."""
        contract = self.dao.create_contract(
            customer_id, sales_contact, total_amount, due_amount, is_signed
        )
        return f"✅ Contrat {contract.id} créé avec succès."

    @require_permission("edit_contracts")
    def update_contract(self, contract_id, **kwargs):
        """Met à jour un contrat existant."""
        contract = self.dao.get_by_id(contract_id)
        if contract.sales_contact != self.user_id or self.user.department_id not in (1, 4) :
            return "❌ Vous n'êtes pas responsable de ce client."
        contract = self.dao.update_contract(contract_id, **kwargs)
        if not contract:
            return "❌ Contrat non trouvé."
        return f"✅ Contrat {contract.id} mis à jour avec succès."
