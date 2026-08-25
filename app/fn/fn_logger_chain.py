"""FN-LOGGERCHAIN | logger obtained via a getter chain is still a log sink."""
import logging

import structlog

from app.models.user import User


def via_std(user: User):
    logging.getLogger(__name__).info(user.aadhaar)   # fires CRITICAL


def via_structlog(user: User):
    structlog.get_logger().info(user.pan)            # fires HIGH
