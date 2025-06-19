# exponential_core\logger\core.py
import logging

def get_logger(name="app") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        console_handler.setFormatter(formatter)

        logger.setLevel(logging.INFO) 
        logger.addHandler(console_handler)

    return logger
