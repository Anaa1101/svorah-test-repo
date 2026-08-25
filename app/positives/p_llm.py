"""P-LLM | pii-to-llm | DPDP-028 | expected: MEDIUM (email)."""
import openai

from app.models.user import User


def triage(user: User):
    return openai.chat.completions.create(model="gpt-4o", messages=user.email)
