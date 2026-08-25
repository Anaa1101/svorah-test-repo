"""P-LOG | pii-in-log | DPDP-002 | expected: CRITICAL (aadhaar)."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    logger.info(user.aadhaar)
