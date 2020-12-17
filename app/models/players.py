from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.common.db_init import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    games = relationship("Game",
                         secondary="players_games",
                         back_populates="players",
                         cascade="all, delete")
