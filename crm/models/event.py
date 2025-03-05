from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship
from models.base import Base


class Event(Base):
    """Represents an event in the system."""

    __tablename__ = "event"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    name = Column(String(255), nullable=False)
    contract_id = Column(Integer, ForeignKey("contract.id", ondelete="CASCADE"), nullable=False, unique=True)
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    support_contact = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text)

    contract = relationship("Contract", back_populates="event")  # Relationship with Contract table 1-1
    support = relationship("User")  # Relationship with User table (support contact)
