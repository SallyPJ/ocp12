from database.transaction_manager import TransactionManager
from models import Department,User, Customer, Contract, Event
from sqlalchemy.orm import Session

class DepartmentDAO:
    """Gestion des accès aux départements."""

    def __init__(self, session: Session):
        """Receives an active session from the caller (no more get_session())."""
        self.session = session

    def get_by_name(self, name):
        """Récupère un département par son nom."""
        return self.session.query(Department).filter_by(name=name).first()

    def get_permissions(self, department_name):
        """Fetches permissions assigned to a given department via department_permissions table."""

        # Step 1️⃣: Get the department ID
        department = self.session.query(Department).filter_by(name=department_name).first()
        if not department:
            return None  # ❌ Department not found

        # Step 2️⃣: Query the department_permissions table directly
        stmt = select(Permission.name).join(department_permissions).where(
            department_permissions.c.department_id == department.id)
        results = self.session.execute(stmt).fetchall()

        # Convert results to a list of permission names
        return [row[0] for row in results]  # ✅ Returns a list of permission names

    def save(self, department):
        """Ajoute un département en base."""
        self.session.add(department)
        self.session.commit()
        return department

class UserDAO:
    """Data Access Object for user management."""

    def __init__(self, session: Session):
        """Receives an active session from the caller (no more get_session())."""
        self.session = session

    def get_by_email(self, email):
        """Fetches a user by email."""
        return self.session.query(User).filter_by(email=email).first()

    def save(self, user):
        """Adds or updates a user in the database."""
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, user):
        """Deletes a user from the database."""
        self.session.delete(user)
        self.session.commit()



class CustomerDAO:
    """Handles database operations for Clients."""

    def __init__(self, session: Session):
        self.session = session

    def get_all_customers(self):
        """Retrieve all clients from the database."""
        return self.session.query(Customer).all()

    def save_customer(self, name, email, phone, enterprise):
        """Ajoute un client en base de données."""
        new_customer = Customer(
            name=name,
            email=email,
            phone=phone,
            enterprise=enterprise
        )
        self.session.add(new_customer)
        self.session.commit()
        return new_customer

class ContractDAO:
    """Handles database operations for Contracts."""

    def __init__(self, session: Session):
        self.session = session

    def get_all_contracts(self):
        """Retrieve all contracts from the database."""
        return self.session.query(Contract).all()

class EventDAO:
    """Handles database operations for Events."""

    def __init__(self, session: Session):
        self.session = session

    def get_all_events(self):
        """Retrieve all events from the database."""
        return self.session.query(Event).all()