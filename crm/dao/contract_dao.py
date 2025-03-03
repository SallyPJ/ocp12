from models.contract import Contract

class ContractDAO:
    """Accès aux données contrats (lecture seule)."""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Récupère tous les contrats."""
        return self.session.query(Contract).all()

    def get_filtered_contracts(self, customer_id=None, is_signed=None, start_date=None, end_date=None,
                               sales_contact=None, is_paid=None):
        """
        Récupère les contrats avec des filtres optionnels :
        - customer_id: ID du client
        - is_signed: Booléen (True/False)
        - start_date: Date de création minimale
        - end_date: Date de création maximale
        - sales_contact: ID du commercial
        """
        query = self.session.query(Contract)

        if customer_id is not None:
            query = query.filter(Contract.customer_id == customer_id)
        if is_signed is not None:
            query = query.filter(Contract.is_signed == is_signed)
        if start_date is not None:
            query = query.filter(Contract.creation_date >= start_date)
        if end_date is not None:
            query = query.filter(Contract.creation_date <= end_date)
        if sales_contact is not None:
            query = query.filter(Contract.sales_contact == sales_contact)
        if is_paid is not None:
            query = query.filter(Contract.due_amount == 0 if is_paid else Contract.due_amount > 0)

        return query.all()
    def get_by_id(self, contract_id):
        """Récupère un contrat par ID."""
        return self.session.query(Contract).filter_by(id=contract_id).first

    def create_contract(self, customer_id, sales_contact, total_amount, due_amount, is_signed):
        """Crée un nouveau contrat."""
        new_contract = Contract(
            customer_id=customer_id,
            sales_contact=sales_contact,
            total_amount=total_amount,
            due_amount=due_amount,
            is_signed=is_signed,
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