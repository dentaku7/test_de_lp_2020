from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.common.db_init import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String, unique=False)
    role = Column(Integer, nullable=False)
    studio_id = Column(Integer, ForeignKey("studios.id"))
    studio = relationship("Studio",
                          back_populates="users",
                          cascade="all, delete")
