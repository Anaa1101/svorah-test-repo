"""FP-COMPOUND | compound-expr 'log' traps and config assignments (not calls) must not fire."""
import openai
import stripe

from app.lib.noise import res
from app.models.user import User


def render_compound(user: User):
    res.render({"loginError": user.email})   # 'loginError' contains 'log'; render is not a sink


def mongo_update(user: User, collection):
    collection.update_one({"_id": 1}, {"$set": {"email": user.email}})  # DB write, not a leak sink


def config_assignment(user: User):
    openai.api_key = user.token   # assignment to a config attr, not a call
    stripe.apiKey = user.token    # assignment to a config attr, not a call
