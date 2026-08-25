"""FP-RECEIVER | PII token on a non-person / temp receiver must NOT fire."""
import logging
from types import SimpleNamespace

from app.lib.infra import cache
from app.lib.noise import challenge, config, table

logger = logging.getLogger(__name__)


def ip_on_config():
    logger.info(config.ipAddress)      # 'address' token but non-person + 'ip' qualifier


def non_person_names():
    cache.set("t", table.name)         # non-person receiver
    cache.set("c", challenge.name)     # non-person receiver


def temp_receiver():
    _tmp_56 = SimpleNamespace(name="anon")
    cache.set("x", _tmp_56.name)       # anonymous/temp receiver, no person context
