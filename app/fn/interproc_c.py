"""FN-INTERPROC (file 3/3) | the sink. The finding is anchored here."""
import logging

logger = logging.getLogger(__name__)


def emit(value):
    logger.info(value)
