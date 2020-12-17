import logging
import socket
from time import sleep

from app.common.db_init import engine, Base
# DB imports for metadata
# noinspection PyUnresolvedReferences
from app.config import ENABLE_CITUS
# noinspection PyUnresolvedReferences
from app.models.players import Player
# noinspection PyUnresolvedReferences
from app.models.studios import Studio
from app.utils.fake_data import (
    run_citus_sql_commands,
    generate_studios,
    generate_games,
    generate_players,
    generate_game_players,
    generate_users
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SetUp")

# Set up tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

if ENABLE_CITUS:
    run_citus_sql_commands()

# Generate fake data
generate_players(1000)
generate_studios(10)
generate_games(10)
generate_game_players()
generate_users()

logger.info("""
*************************
****** SET UP DONE ******
*************************
""")

# For the correct container startup sequence
addr = ("", 11111)
s = socket.create_server(addr)
while True:
    sleep(1)
