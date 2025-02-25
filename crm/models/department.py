from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.permission import Permission

# 📌 Table d'association Many-to-Many entre Department et Permission
department_permissions = Table(
    "department_permissions",
    Base.metadata,
    Column("department_id", Integer, ForeignKey("department.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id", ondelete="CASCADE"), primary_key=True),
)

class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False)

    # Relation Many-to-Many avec les permissions
    permissions = relationship("Permission", secondary=department_permissions, backref="departments")

    def __repr__(self):
        return f"<Department {self.name}>"