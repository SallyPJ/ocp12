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
    Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

#Association table for many-to-many relationship between departements and permissions
department_permissions = Table(
    "department_permissions",
    Base.metadata,
    Column("department_id", Integer, ForeignKey("department.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)




class Department(Base):
    __tablename__ = 'department'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    name = Column(String(30), unique=True, nullable=False)
    permissions = relationship("Permission", secondary=department_permissions, backref="departments")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    name = Column(String(255), unique=True,  nullable=False)

# Enumération des permissions



# 📌 Modèle Contrat
 # Relation vers le customer


# 📌 Modèle Event
