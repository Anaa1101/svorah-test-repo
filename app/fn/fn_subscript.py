"""FN-SUBSCRIPT | subscript access is still a PII source."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User, body: dict):
    logger.info(user["aadhaar"])   # fires CRITICAL
    logger.info(body['email'])     # fires MEDIUM
