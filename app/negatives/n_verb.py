"""N-VERB | sanitiser layer 1 (verb) | pairs P-LOG | expected: 0 findings."""
import logging

from app.lib.sanitizers import mask
from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    logger.info(mask(user.email))
