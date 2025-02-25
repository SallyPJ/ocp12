from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship
from models.base import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)  # "+33612345678"
    enterprise = Column(String(255))
    creation_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    last_update = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    sales_contact = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))  # Lien avec Sales
    sales_rep = relationship("User")  # Relation vers l'utilisateur commercial
