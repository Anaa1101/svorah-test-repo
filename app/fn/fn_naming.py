"""FN-NAMING | camelCase / snake / suffix variants are the same PII, must still match."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    logger.info(user.aadhaarNumber)   # fires CRITICAL
    logger.info(user.emailAddress)    # fires MEDIUM
    logger.info(user.user_phone)      # fires MEDIUM
