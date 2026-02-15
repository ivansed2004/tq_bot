import logging
from logging.handlers import RotatingFileHandler
import os

logging.getLogger("httpx").setLevel(logging.WARNING)

LOG_DIRECTORY=os.getenv("LOG_DIRECTORY")
LOG_FILE=os.getenv("LOG_FILE")
LOG_MESSAGE_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_TIME_FORMAT="%Y-%m-%d %H:%M:%S"

LOG_FILE_MAX_SIZE = 5 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 5

if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIRECTORY, LOG_FILE),
    mode='a',
    maxBytes=LOG_FILE_MAX_SIZE,
    backupCount=LOG_FILE_BACKUP_COUNT
)

logging.basicConfig(
    filename=os.path.join(LOG_DIRECTORY, LOG_FILE),
    level=logging.INFO,
    format=LOG_MESSAGE_FORMAT,
    datefmt=LOG_TIME_FORMAT
)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(file_handler)