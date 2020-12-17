from sqlalchemy import func, desc

from app.models.games import Game
from app.models.player_games import PlayerGame
from app.models.players import Player
from app.models.studios import Studio
from app.models.users import User
from app.schemas.games import GameNameIn
from app.schemas.users import UserIn


def get_user(db, user: UserIn):
    return db.query(User).filter(User.id == user.id).first()


def studio_add_game(db, user: User, game: GameNameIn):
    db_game = Game(name=game.name, studio_id=user.studio_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_games_popularity(db):
    query = (db
        .query(Game)
        .join(PlayerGame)
        .join(Studio)
        .group_by(Game.id, Game.name, Studio.id)
        .order_by(desc("players_count"))
        .values(
        Game.id.label("id"),
        Game.name.label('name'),
        func.count(PlayerGame.id).label("players_count"),
        Studio.id.label("studio_id"),
        Studio.name.label("studio_name"))
    )

    return query


def get_studio_players(db, studio_id, studio_name):
    query = (db
             .query(Game)
             .join(PlayerGame)
             .join(Player)
             .filter((Game.studio_id == studio_id)
                     |
                     (Studio.name == studio_name)
                     )
             )
    return query.all()
