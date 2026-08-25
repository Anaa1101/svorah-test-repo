"""ORD-BEFOREAFTER | sanitiser position matters (flow order, not mere presence)."""
import logging

from app.lib.sanitizers import mask
from app.models.user import User

logger = logging.getLogger(__name__)


def sanitise_before(user: User):
    x = mask(user.pan)
    logger.info(x)          # suppressed (masked before the sink)


def sanitise_after(user: User):
    logger.info(user.pan)   # FIRES HIGH (leak happens before the mask)
    y = mask(user.pan)
    return y
