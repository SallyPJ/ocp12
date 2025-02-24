from passlib.hash import argon2
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from models.base import Base
from models.department import Department


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    _password = Column("password", String(255), nullable=False)

    def __init__(self, first_name, last_name, email, department_id, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department_id = department_id
        self.password = password

    @property
    def password(self):
        raise AttributeError("Le mot de passe est en écriture seule.")

    @password.setter
    def password(self, plain_password):
        """Hache le mot de passe avec Argon2 avant de le stocker."""
        self._password = argon2.hash(plain_password)

    def check_password(self, password):
        """Vérifie si un mot de passe correspond au hash stocké."""
        return argon2.verify(password, self._password)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.email})>"