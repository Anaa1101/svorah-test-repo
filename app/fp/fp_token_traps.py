"""FP-TOKENS | token equality, not substring; field-name-about-PII is not a PII value."""
import logging

from app.lib.noise import dobson, email_regex, email_template_id, expand, nameField

logger = logging.getLogger(__name__)


def substring_traps(x):
    logger.info(expand(x))          # 'pan' inside 'expand' must not match
    logger.info(dobson.value)       # 'dob' inside 'dobson' must not match


def field_name_not_value():
    logger.info(email_regex)        # a regex about email, not an email value
    logger.info(email_template_id)  # a template id, not an email value
    logger.info(nameField)          # the string "name", not a person's name
