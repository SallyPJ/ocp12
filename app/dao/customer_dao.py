from models.customer import Customer

class CustomerDAO:
    """Accès aux données clients (lecture seule)."""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Récupère tous les clients."""
        return self.session.query(Customer).all()

    def get_by_id(self, customer_id):
        """Récupère un client par ID."""
        return self.session.query(Customer).filter_by(id=customer_id).first()

    def create(self, name, email, phone, enterprise, sales_contact):
        """Crée un nouveau client."""
        new_customer = Customer(
            name=name,
            email=email,
            phone=phone,
            enterprise=enterprise,
            sales_contact=sales_contact
        )
        self.session.add(new_customer)
        self.session.commit()
        return new_customer

    def update(self, customer_id, **kwargs):
        """Met à jour un client si l'utilisateur est responsable."""
        customer = self.get_by_id(customer_id)
        if not customer:
            return None
        for key, value in kwargs.items():
            setattr(customer, key, value)
        self.session.commit()
        return customer