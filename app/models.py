from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(String,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP,server_default=text("now()"),nullable=False)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True,nullable=False)
    name = Column(String, index=True,nullable=False,unique=True)
    project_manager_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_at = Column(TIMESTAMP,server_default=text("now()"),nullable=False)

    project_manager = relationship("User", foreign_keys=[project_manager_id])
    client = relationship("User", foreign_keys=[client_id])