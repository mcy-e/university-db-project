import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from colorlog import ColoredFormatter

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    if root.handlers:
        return

    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(file_formatter)


    console_formatter = ColoredFormatter(
        "%(cyan)s%(asctime)s%(reset)s | "
        "%(log_color)s%(levelname)-8s%(reset)s | "
        "%(blue)s%(name)s%(reset)s | "
        "%(white)s%(message)s%(reset)s",
        datefmt="%H:%M:%S",
        log_colors={
            "DEBUG":    "purple",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        },
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    root.addHandler(file_handler)
    root.addHandler(console_handler)
