from models.contract import Contract

class ContractDAO:
    """Accès aux données contrats (lecture seule)."""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Récupère tous les contrats."""
        return self.session.query(Contract).all()

    def get_by_id(self, contract_id):
        """Récupère un contrat par ID."""
        return self.session.query(Contract).filter_by(id=contract_id).first