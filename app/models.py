from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    Date,
    Text,
    TIMESTAMP,
    DateTime,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=True,
        unique=True,
    )
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50))  # Type de l'utilisateur (sales, support, admin)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": role,  # Détermine le type de sous-classe
    }


class Sales(User):
    __mapper_args__ = {"polymorphic_identity": "sales"}


class Support(User):
    __mapper_args__ = {"polymorphic_identity": "support"}


class Admin(User):
    __mapper_args__ = {"polymorphic_identity": "admin"}


class Customer(Base):
    __tablename__ = "customer"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=True,
        unique=True,
    )
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)  # Format international recommandé
    enterprise = Column(String(255))
    creation_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    last_update = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    sales_contact = Column(Integer, ForeignKey("user.id"), nullable=False)  # Lien avec Sales

    sales_rep = relationship("User")  # Relation vers l'utilisateur commercial


# 📌 Modèle Contrat
class Contract(Base):
    __tablename__ = "contract"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=True,
        unique=True,
    )
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    sales_contact = Column(Integer, ForeignKey("user.id"), nullable=False)  # Doit être un commercial
    total_amount = Column(Integer, nullable=False)
    due_amount = Column(Integer, nullable=False)
    creation_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    status = Column(Enum("signed", "not_signed"), nullable=False)  # ENUM pour statut

    customer = relationship("Customer")  # Relation vers le customer


# 📌 Modèle Event
class Event(Base):
    __tablename__ = "event"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=True,
        unique=True,
    )
    name = Column(String(255), nullable=False)
    contract_id = Column(Integer, ForeignKey("contract.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    support_contact = Column(Integer, ForeignKey("user.id"), nullable=True)  # Peut être NULL si non assigné
    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text)

    contract = relationship("Contract")  # Relation vers Contrat
    support = relationship("User")  # Relation vers Support
