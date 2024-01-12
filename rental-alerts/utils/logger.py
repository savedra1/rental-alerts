
import logging

def set_up_logger() -> logging:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    return logger

def alert_admin(err=None):
    pass