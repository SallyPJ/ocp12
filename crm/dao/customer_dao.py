from models.customer import Customer
from sqlalchemy.orm import joinedload


class CustomerDAO:
    """Accès aux données clients (lecture seule)."""

    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Retrieves all customers"""
        return self.session.query(Customer).options(joinedload(Customer.sales_rep)).all()

    def get_by_id(self, customer_id):
        """Retrieves a customer by ID"""
        return self.session.query(Customer).filter_by(id=customer_id).first()

    def create(self, first_name, last_name, email, phone, enterprise, sales_contact):
        """Creates a new customer"""
        new_customer = Customer(
            first_name=first_name,last_name=last_name, email=email, phone=phone,
            enterprise=enterprise, sales_contact=sales_contact, last_update=None
        )
        self.session.add(new_customer)
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
