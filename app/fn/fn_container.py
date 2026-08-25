"""FN-CONTAINER | PII wrapped in a dict/list still reaches the sink."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    logger.info({"aadhaar": user.aadhaar})   # fires CRITICAL
