"""N-CRYPTO | sanitiser layer 2 (crypto lib) | pairs P-LOG | expected: 0 findings.
The Java half lives in app/java/com/svorah/testrepo/NCrypto.java (Cipher.doFinal)."""
import logging

import bcrypt

from app.models.user import User

logger = logging.getLogger(__name__)


def handle(user: User):
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    logger.info(hashed)
