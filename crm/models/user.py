from passlib.hash import argon2
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
)
from models.base import Base
from models.department import Department



class User(Base):
    """Represents an employee in the system."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("department.id", ondelete="SET NULL"))
    department = relationship("Department", back_populates="users")
    _password = Column("password", String(255), nullable=False)
    active = Column(Boolean, default=True)

    def __init__(self, first_name, last_name, email, department_id, password, active):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department_id = department_id
        self.password = password
        self.active = active

    @property
    def password(self):
        """Prevents direct access to the password attribute."""
        raise AttributeError("Le mot de passe est en écriture seule.")

    @password.setter
    def password(self, plain_password):
        """Hashes the password using Argon2 before storing it."""
        self._password = argon2.hash(plain_password)

    def check_password(self, password):
        """Verifies if a given password matches the stored hash."""
        return argon2.verify(password, self._password)

    def __repr__(self):
        """Returns a string representation of the user."""
        return f"<User {self.first_name} {self.last_name} ({self.email})>"
