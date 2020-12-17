from app.common.fastapi_app import get_app
# DB imports for metadata
# noinspection PyUnresolvedReferences
from app.models.games import Game
# noinspection PyUnresolvedReferences
from app.models.players import Player
# noinspection PyUnresolvedReferences
from app.models.studios import Studio
# noinspection PyUnresolvedReferences
from app.models.player_games import PlayerGame
from app.routers.auth import players_router
from app.routers.players import router

app = get_app()

URL_PREFIX = '/players'
app.include_router(players_router, prefix=URL_PREFIX)
app.include_router(router, prefix=URL_PREFIX)
