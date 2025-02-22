from db.transaction_manager import TransactionManager
from models import Department,User
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