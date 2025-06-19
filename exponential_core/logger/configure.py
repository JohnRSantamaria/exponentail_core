import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter

_logger_initialized = False  # Protección global

def configure_logging(log_level="INFO", log_file="logs/errors.log"):
    global _logger_initialized
    if _logger_initialized:
        return logging.getLogger("app")

    # Convertir a Path y asegurar ruta absoluta
    log_file = Path(log_file).resolve()
    log_dir = log_file.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # File handler con rotación
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(pathname)s:%(lineno)d | %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler con colores
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

    # Configurar logger principal
    logger = logging.getLogger("app")
    logger.setLevel(log_level)

    # Limpia handlers anteriores
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    _logger_initialized = True
    return logger
