from .configure import configure_logging

# Esto se ejecuta solo una vez al importar exponential_core.logger
logger = configure_logging()