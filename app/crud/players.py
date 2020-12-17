import uuid

from sqlalchemy.orm import Session, joinedload

from app.crud.common import UserIsAlreadyRegisteredException
from app.models.games import Game
from app.models.players import Player
from app.schemas.games import GameIn
from app.schemas.players import PlayerOut




def get_player(db, player: PlayerOut):
    db_player = db.query(Player).filter(Player.id == player.id).first()
    return db_player


def register_player(db: Session, name, hashed_password):
    db_player = db.query(Player).filter(Player.name == name).first()
    if db_player:
        raise UserIsAlreadyRegisteredException()
    player = Player(name=name, password=hashed_password)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def delete_player(db: Session, player_id):
    db_player = db.query(Player).filter(Player.id == player_id).first()
    db_player.name = f"rnd-{uuid.uuid4()}"
    db.add(db_player)
    db.commit()


def get_player_games(db, player: PlayerOut):
    return (db
            .query(Player)
            .options(joinedload(Player.games))
            .filter(Player.id == player.id).all()
            )


def player_register_game(db, player: PlayerOut, game: GameIn):
    db_player = get_player(db, player)
    db_game = (db
               .query(Game)
               .filter((Game.id == game.id)
                       |
                       (Game.name == game.name)
                       )
               .first()
               )
    db_player.games.append(db_game)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return db_player


def player_unregister_game(db, player: PlayerOut, game: GameIn):
    db_player = db.query(Player).filter(Player.id == player.id).first()
    for g in db_player.games:
        if g.id == game.id or g.name == game.name:
            db_player.games.remove(g)
    db.commit()
    db.refresh(db_player)

    return db_player
