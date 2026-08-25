"""N-EXCLUDED | path exclusion | expected: 0 findings.
This is a genuine PII->log flow (identical to P-LOG) but it lives under tests/**,
which .svorah.yml excludes, so the scanner must not report it."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    logger.info(user.aadhaar)
