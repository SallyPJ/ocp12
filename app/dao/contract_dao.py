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

    def create_contract(self, customer_id, sales_contact, total_amount, due_amount, status):
        """Crée un nouveau contrat."""
        new_contract = Contract(
            customer_id=customer_id,
            sales_contact=sales_contact,
            total_amount=total_amount,
            due_amount=due_amount,
            status=status,
        )
        self.session.add(new_contract)
        self.session.commit()
        return new_contract

    def update_contract(self, contract_id, **kwargs):
        """Met à jour un contrat existant."""
        contract = self.get_by_id(contract_id)
        if not contract:
            return None

        for key, value in kwargs.items():
            if hasattr(contract, key):
                setattr(contract, key, value)

        self.session.commit()
        return contract