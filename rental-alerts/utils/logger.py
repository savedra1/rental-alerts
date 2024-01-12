
import logging
from utils.email_client import send_email

def set_up_logger() -> logging:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    return logger

def alert_admin(err_msg) -> str:
    response = send_email(err_msg, subject='AN ERROR OCURRED WHEN FETCHING NEW PROPERTY DATA.')
    return response