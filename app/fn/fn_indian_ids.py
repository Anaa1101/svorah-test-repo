"""FN-INDIANIDS | the India-first moat: UPI / IFSC / voter-id / PAN fire with severity."""
import logging

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    logger.info(user.upi)       # fires HIGH   (upi_id)
    logger.info(user.ifsc)      # fires MEDIUM (IFSC = public bank-branch code, not an account number)
    logger.info(user.voterId)   # fires HIGH   (voter_id)
    logger.info(user.pan)       # fires HIGH   (pan)
