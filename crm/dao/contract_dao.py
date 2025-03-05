from models.contract import Contract


class ContractDAO:
    """Access to the contract"""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Retrieves all contracts"""
        return self.session.query(Contract).all()

    def get_by_id(self, contract_id):
        """Retrieves a contract by ID"""
        return self.session.query(Contract).filter_by(id=contract_id).first()

    def get_filtered_contracts(self, customer_id=None, is_signed=None, sales_contact=None, is_paid=None):
        """
        Retrieves contracts based on optional filters
        """
        query = self.session.query(Contract)

        if customer_id is not None:
            query = query.filter(Contract.customer_id == customer_id)
        if is_signed is not None:
            query = query.filter(Contract.is_signed == is_signed)
        if sales_contact is not None:
            query = query.filter(Contract.sales_contact == sales_contact)
        if is_paid is not None:
            query = query.filter(Contract.due_amount == 0 if is_paid else Contract.due_amount > 0)

        return query.all()

    def create_contract(self, customer_id, sales_contact, total_amount, due_amount, is_signed):
        """Creates a new contract"""
        new_contract = Contract(
            customer_id=customer_id,
            sales_contact=sales_contact,
            total_amount=total_amount,
            due_amount=due_amount,
            is_signed=is_signed,
        )
        self.session.add(new_contract)
        return new_contract

    def update_contract(self, contract_id, **kwargs):
        """Updates an existing contract"""
        contract = self.get_by_id(contract_id)
        if not contract:
            return None

        for key, value in kwargs.items():
            if hasattr(contract, key):
                print(f"✅ Mise à jour {key} -> {value}")

                setattr(contract, key, value)

        return contract
