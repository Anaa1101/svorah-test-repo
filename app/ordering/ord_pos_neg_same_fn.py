"""ORD-POSNEG | a positive and a matched sanitised negative in one function -> ONE finding."""
import logging

from app.lib.sanitizers import mask
from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    logger.info(user.pan)             # FIRES HIGH
    logger.info(mask(user.email))     # suppressed
