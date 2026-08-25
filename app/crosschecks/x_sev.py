"""X-SEV | severity = PII harm tier, not the rule.
Same rule (pii-in-log) and same sink, three PII fields -> three severities."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    logger.info(user.aadhaar)   # expected: CRITICAL
    logger.info(user.pan)       # expected: HIGH
    logger.info(user.email)     # expected: MEDIUM
