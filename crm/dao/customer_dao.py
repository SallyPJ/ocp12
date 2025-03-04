from models.customer import Customer


class CustomerDAO:
    """Accès aux données clients (lecture seule)."""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Retrieves all customers"""
        return self.session.query(Customer).all()

    def get_by_id(self, customer_id):
        """Retrieves a customer by ID"""
        return self.session.query(Customer).filter_by(id=customer_id).first()

    def create(self, name, email, phone, enterprise, sales_contact):
        """Creates a new customer"""
        new_customer = Customer(name=name, email=email, phone=phone, enterprise=enterprise, sales_contact=sales_contact)
        self.session.add(new_customer)
        self.session.commit()
        return new_customer

    def update(self, customer_id, **kwargs):
        """Updates an existing customer."""
        customer = self.get_by_id(customer_id)
        if not customer:
            return None
        for key, value in kwargs.items():
            setattr(customer, key, value)
        self.session.commit()
        return customer
