from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from app.common.db_init import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    studio_id = Column(Integer, ForeignKey("studios.id"))
    studio = relationship("Studio",
                          back_populates="games",
                          cascade="all, delete")
    players = relationship("Player",
                           secondary="players_games",
                           back_populates="games",
                           cascade="all, delete")
