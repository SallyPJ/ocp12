from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Boolean,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship
from models.base import Base


class Contract(Base):
    """Represents a contract in the system."""

    __tablename__ = "contract"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="CASCADE"), nullable=False)
    sales_contact = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))  # Doit être un commercial
    total_amount = Column(Integer, nullable=False)
    due_amount = Column(Integer, nullable=False)
    creation_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    is_signed = Column(Boolean, nullable=False, default=False)
    customer = relationship("Customer", backref="contracts")
    sales_contact_user = relationship("User", backref="contracts")

    event = relationship("Event", back_populates="contract", uselist=False)

    @property
    def is_paid(self):
        """Returns True if the contract is fully paid (due amount = 0), otherwise False."""
        return self.due_amount == 0
