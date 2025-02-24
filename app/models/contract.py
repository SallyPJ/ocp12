from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship
from models.base import Base

class Contract(Base):
    __tablename__ = "contract"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    sales_contact = Column(Integer, ForeignKey("user.id"), nullable=False)  # Doit être un commercial
    total_amount = Column(Integer, nullable=False)
    due_amount = Column(Integer, nullable=False)
    creation_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    status = Column(Enum("signed", "not_signed"), nullable=False)  # ENUM pour statut
    customer = relationship("Customer")