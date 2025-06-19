import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter


def configure_logging(log_level="INFO", log_file="logs/errors.log"):
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(pathname)s:%(lineno)d | %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    color_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(pathname)s:%(lineno)d | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        style="%",
    )
    console_handler.setFormatter(color_formatter)

    logger = logging.getLogger("app")
    logger.setLevel(log_level)


    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
