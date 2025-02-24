from sqlalchemy.orm import Session
from models.user import User

class UserDAO:
    """Data Access Object pour la gestion des utilisateurs."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    def get_by_id(self, user_id):
        return self.session.query(User).filter_by(id=user_id).first()

    def get_all(self):
        return self.session.query(User).all()

    def exists(self, email):
        return self.get_by_email(email) is not None

    def save(self, user):
        self.session.add(user)

    def delete(self, user):
        self.session.delete(user)

    def update(self, user, **kwargs):
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)