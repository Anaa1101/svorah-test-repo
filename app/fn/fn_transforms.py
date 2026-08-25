"""FN-TRANSFORMS | non-sanitising wrappers must NOT launder PII — each still fires.
str(), f-strings and .strip() change representation, not sensitivity."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def via_str(user: User):
    logger.info(str(user.aadhaar))        # fires CRITICAL


def via_fstring(user: User):
    logger.info(f"{user.pan}")            # fires HIGH


def via_strip(user: User):
    logger.info(user.email.strip())       # fires MEDIUM
