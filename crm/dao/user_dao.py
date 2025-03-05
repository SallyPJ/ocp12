from sqlalchemy.orm import Session
from models.user import User


class UserDAO:
    """Data Access Object pour la gestion des utilisateurs."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        """Retrieves all users"""
        return self.session.query(User).all()

    def get_by_email(self, email):
        """Retrieves a user by email"""
        return self.session.query(User).filter_by(email=email).first()

    def get_by_id(self, user_id):
        """Retrieves a user by id"""
        return self.session.query(User).filter_by(id=user_id).first()

    def exists(self, email):
        """Checks if a user exists by email"""
        return self.get_by_email(email) is not None

    def create(self, first_name, last_name, email, password, department_id, active=True):
        """Creates a new user and stores it in the database"""
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department_id,
            password=password,
            active=active,
        )
        self.session.add(new_user)
        return new_user

    def update(self, user, **kwargs):
        """Updates an existing user with given attributes"""
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

    def delete(self, user):
        """Deletes a user from the database"""
        self.session.delete(user)

    def deactivate_user(self, user_id):
        """Deactivates a user (e.g., resignation)"""
        user = self.get_by_id(user_id)
        if user:
            user.active = False
