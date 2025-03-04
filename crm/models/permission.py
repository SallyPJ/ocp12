from sqlalchemy import Column, Integer, String
from models.base import Base


class Permission(Base):
    """Represents a permission in the system."""

    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        """Returns a string representation of the permission."""
        return f"<Permission {self.name}>"
