from sqlalchemy import ForeignKey, Column, Integer, UniqueConstraint

from app.common.db_init import Base


class PlayerGame(Base):
    __tablename__ = "players_games"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)

    __table_args__ = (UniqueConstraint(player_id, game_id),)
