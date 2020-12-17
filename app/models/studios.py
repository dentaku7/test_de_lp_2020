from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.common.db_init import Base


class Studio(Base):
    __tablename__ = "studios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    games = relationship("Game", back_populates="studio", cascade="all, delete")
    users = relationship("User",
                         back_populates="studio",
                         cascade="all, delete")
