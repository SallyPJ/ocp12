from dao.contract_dao import ContractDAO
from services.permissions import require_permission
from controllers.base_controller import BaseController
class ContractController(BaseController):
    """Gère les contrats en lecture seule."""

    def __init__(self, session):
        super().__init__(session, ContractDAO)

    @require_permission("read_all_contracts")
    def list_contracts(self):
        """Retourne la liste de tous les contrats."""
        contracts = self.contract_dao.get_all()
        if not contracts:
            return ["Aucun contrat trouvé."]
        return [f"{c.id} - Client ID: {c.customer_id}, Montant: {c.total_amount}€, Statut: {c.status}"
                for c in contracts]

    @require_permission("read_all_contracts")
    def get_contract(self, contract_id):
        """Retourne un contrat spécifique."""
        contract = self.contract_dao.get_by_id(contract_id)
        if not contract:
            return "❌ Contrat non trouvé."
        return (f"Contrat {contract.id} - Client ID: {contract.customer_id}, Montant: {contract.total_amount}€,"
                f" Statut: {contract.status}")

    @require_permission("create_contracts")
    def create_contract(self, customer_id, sales_contact, total_amount, due_amount, status):
        """Crée un nouveau contrat."""
        contract = self.dao.create_contract(
            customer_id, sales_contact, total_amount, due_amount, status
        )
        return f"✅ Contrat {contract.id} créé avec succès."

    @require_permission("edit_all_contracts")
    def update_contract(self, contract_id, **kwargs):
        """Met à jour un contrat existant."""
        contract = self.dao.update_contract(contract_id, **kwargs)
        if not contract:
            return "❌ Contrat non trouvé."
        return f"✅ Contrat {contract.id} mis à jour avec succès."
