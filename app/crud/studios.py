from sqlalchemy import func, desc

from app.crud.common import UserNotFound
from app.models.games import Game
from app.models.player_games import PlayerGame
from app.models.players import Player
from app.models.studios import Studio
from app.models.users import User
from app.schemas.games import GameNameIn
from app.schemas.players import PlayerGameIn


def get_studio(db, studio_id):
    return db.query(Studio).filter(Studio.id == studio_id).first()


def studio_add_game(db, user: User, game: GameNameIn):
    db_game = Game(name=game.name, studio_id=user.studio_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_studio_games_popularity(db, studio_id):
    query = (db
        .query(Game)
        .join(PlayerGame)
        .group_by(Game.id, Game.name)
        .filter(Game.studio_id == studio_id)
        .order_by(desc("players_count"))
        .values(
        Game.id.label("id"),
        Game.name.label('name'),
        func.count(PlayerGame.id).label("players_count"))
    )
    return query


def get_studio_players(db, studio_id):
    query = (db
             .query(Game)
             .join(PlayerGame)
             .join(Player)
             .filter(Game.studio_id == studio_id)
             )
    return query.all()


def studio_game_register_player(db, pg: PlayerGameIn):
    db_game = db.query(Game).filter(Game.id == pg.game_id).first()
    db_player = db.query(Player).filter(Player.id == pg.player_id).first()
    if not db_player:
        raise UserNotFound()
    db_game.players.append(db_player)
    db.commit()
    db.refresh(db_game)
    return db_game


def studio_game_unregister_player(db, pg: PlayerGameIn):
    db_game = db.query(Game).filter(Game.id == pg.game_id).first()
    db_player = db.query(Player).filter(Player.id == pg.player_id).first()
    try:
        db_game.players.remove(db_player)
    except ValueError:
        pass
    db.commit()
    db.refresh(db_game)

    return db_game
