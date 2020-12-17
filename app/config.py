import csv
import hashlib
from distutils.util import strtobool
from os import environ
from pathlib import Path

DB_HOST = environ.get("DB_HOST", 'localhost')
DB_PORT = int(environ.get('DB_PORT', '5432'))
DB_NAME = environ.get('DB_NAME', 'postgres')
DB_USER = environ.get('DB_USER', 'postgres')
DB_PSWD = environ.get('DB_PSWD', 'postgres')
DB_SSL_MODE = environ.get('DB_SSL_MODE', 'prefer')

DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(
    DB_USER, DB_PSWD, DB_HOST, DB_PORT, DB_NAME, DB_SSL_MODE)

ENABLE_CITUS = strtobool(environ.get('ENABLE_CITUS', 'false'))

DATA_DIR = Path(environ.get('DATA_DIR', 'fake_data'))

PUBLISHER_API_SECRET_KEY = hashlib.sha1("publisher_api_v1".encode('utf-8')).hexdigest()
PLAYERS_API_SECRET_KEY = hashlib.sha1("players_api_v1".encode('utf-8')).hexdigest()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

AUTH_ROLES = {
    'publisher': 1,
    'studio_owner': 2
}

UNHASHED_PASS = "123456"

CSV_OPTIONS = {'delimiter': ',',
               'quotechar': '\\',
               'quoting': csv.QUOTE_MINIMAL}
