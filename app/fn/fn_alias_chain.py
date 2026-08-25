"""FN-ALIAS | taint must survive a chain of plain assignments."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    a = user.aadhaar
    b = a
    logger.info(b)   # fires CRITICAL
