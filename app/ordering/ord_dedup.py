"""ORD-DEDUP | the same flow through several intermediate vars is ONE finding, not many."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    a = user.aadhaar
    b = a
    c = b
    logger.info(c)   # exactly ONE finding (dedup per file:line)
