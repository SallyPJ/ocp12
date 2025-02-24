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

