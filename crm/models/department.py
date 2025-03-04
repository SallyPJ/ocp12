from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.permission import Permission

# Many-to-Many association table between Department and Permission
department_permissions = Table(
    "department_permissions",
    Base.metadata,
    Column("department_id", Integer, ForeignKey("department.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id", ondelete="CASCADE"), primary_key=True),
)


class Department(Base):
    """Represents a department in the system."""

    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False)

    users = relationship("User", back_populates="department")

    # Many-to-Many relationship with permissions
    permissions = relationship("Permission", secondary=department_permissions, backref="departments")

    def __repr__(self):
        """Returns a string representation of the department."""
        return f"<Department {self.name}>"
