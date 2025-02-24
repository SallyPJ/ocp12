from dao.contract_dao import ContractDAO

class ContractController:
    """Gère les contrats en lecture seule."""

    def __init__(self, session):
        self.contract_dao = ContractDAO(session)

    def list_contracts(self):
        """Retourne la liste de tous les contrats."""
        contracts = self.contract_dao.get_all()
        if not contracts:
            return ["Aucun contrat trouvé."]
        return [f"{c.id} - Client ID: {c.customer_id}, Montant: {c.total_amount}€, Statut: {c.status}" for c in contracts]

    def get_contract(self, contract_id):
        """Retourne un contrat spécifique."""
        contract = self.contract_dao.get_by_id(contract_id)
        if not contract:
            return "❌ Contrat non trouvé."
        return f"Contrat {contract.id} - Client ID: {contract.customer_id}, Montant: {contract.total_amount}€, Statut: {contract.status}"
