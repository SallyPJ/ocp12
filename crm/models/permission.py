from sqlalchemy import Column, Integer, String
from models.base import Base  # ✅ Import de Base

class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Permission {self.name}>"