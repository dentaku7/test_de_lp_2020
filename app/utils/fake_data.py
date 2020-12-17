import csv
import logging
import random
from pathlib import Path
from time import sleep

from faker import Faker

from app.common.auth import get_hashed_password
from app.common.db_init import SessionLocal
from app.config import DATA_DIR, UNHASHED_PASS, CSV_OPTIONS
from app.models.games import Game
from app.models.player_games import PlayerGame
from app.models.players import Player
from app.models.studios import Studio
from app.models.users import User

GENRE = ['Adventure',
         'RPG',
         'Shooter',
         'Survival',
         'Fighter',
         'Battle Royale',
         'Match-3',
         'Beat\' em up',
         'Stealth']

PASS = get_hashed_password(UNHASHED_PASS)

logger = logging.getLogger('FakeDataGenerator')


def generate_players(n):
    logger.info(f"Generating {n} players")
    fake = Faker()
    db = SessionLocal()
    rows = []
    for _ in range(n):
        rows.append(Player(name=fake.user_name(), password=PASS))
    db.bulk_save_objects(rows)
    db.commit()

    with open(DATA_DIR / Path('players.csv'), 'w') as csv_file:
        csv_writer = csv.writer(csv_file, **CSV_OPTIONS)
        for player in rows:
            csv_writer.writerow([player.name, UNHASHED_PASS])


def generate_studios(n):
    logger.info(f"Generating {n} studios")
    fake = Faker()
    db = SessionLocal()
    rows = []
    for _ in range(n):
        rows.append(Studio(name=f"{fake.company()} Games"))
    db.bulk_save_objects(rows)
    db.commit()


def generate_games(n):
    logger.info(f"Generating from 1 to {n} games per studio")
    fake = Faker()
    db = SessionLocal()
    rows = []
    for studio in db.query(Studio).all():
        for _ in range(random.randint(1, n)):
            suffix = random.choice(GENRE)
            name = f"{fake.sentence(3).strip('.').lower().title()} {suffix}"
            rows.append(Game(studio_id=studio.id, name=name))
    db.bulk_save_objects(rows)
    db.commit()


def generate_game_players():
    logger.info(f"Registering players for each game")
    db = SessionLocal()
    players = db.query(Player).all()
    games = db.query(Game).all()
    rows = []
    for player in players:
        random.shuffle(games)
        for game in games[:random.randint(0, len(games))]:
            rows.append(PlayerGame(player_id=player.id, game_id=game.id))
    db.bulk_save_objects(rows)
    db.commit()


def generate_users():
    logger.info("Generate publisher account and user accounts for each studio")
    faker = Faker()
    db = SessionLocal()
    rows = [User(username="owner", password=PASS, role=1)]
    studios = db.query(Studio).all()
    for studio in studios:
        rows.append(User(username=faker.user_name(), password=PASS, role=2, studio_id=studio.id))
    db.bulk_save_objects(rows)
    db.commit()

    with open(DATA_DIR / Path('users.csv'), 'w') as csv_file:
        csv_writer = csv.writer(csv_file, **CSV_OPTIONS)
        for user in rows:
            csv_writer.writerow([user.username, UNHASHED_PASS, user.role, user.studio_id])


def run_citus_sql_commands():
    logger.info("Running Citus SQL commands")
    db = SessionLocal()
    while not db.execute("SELECT * FROM master_get_active_worker_nodes();").first():
        sleep(5)

    db.execute("ALTER TABLE players_games DROP CONSTRAINT players_games_pkey;")

    db.execute("SELECT create_reference_table('studios');")
    db.execute("SELECT create_reference_table('games');")
    db.execute("SELECT create_distributed_table('players', 'id');")
    db.execute("SELECT create_distributed_table('players_games', 'player_id');")

    db.commit()
