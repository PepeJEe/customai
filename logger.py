import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("__name__")
logger.setLevel(level=logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=1_000_000,
    backupCount=3
)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(levelname)8s | %(filename)s - %(lineno)8d | %(message)s")
