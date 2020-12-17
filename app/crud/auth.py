from app.models.players import Player
from app.models.users import User


def get_player_by_id(db, player_id):
    return db.query(Player).filter(Player.id == player_id).first()


def get_player_by_name(db, name):
    return db.query(Player).filter(Player.name == name).first()


def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db, username):
    return db.query(User).filter(User.username == username).first()
