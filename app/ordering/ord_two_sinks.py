"""ORD-TWOSINKS | one line, two distinct sinks -> two findings (log + cache)."""
import logging

from app.lib.infra import cache
from app.models.user import User

logger = logging.getLogger(__name__)


def leak_twice(user: User):
    logger.info(user.email); cache.set("k", user.email)   # two findings on this line
