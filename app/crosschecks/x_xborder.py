"""X-XBORDER | the code agent names the RECIPIENT and labels cross-border SUSPECTED,
never confirmed. Residency is a runtime/infra fact the code cannot see, so the verdict
is deferred to the cloud scan, a .svorah.yml `data_residency` declaration, or the DPO.

cross_border values the code agent may emit:
  suspected | not_suspected | resolved_domestic | not_asserted   (never: confirmed/true)
"""
import openai
import razorpay
import stripe

from app.lib.noise import api_client
from app.models.user import User


def foreign_hq_vendor(user: User):
    openai.chat.completions.create(model="gpt-4o", messages=user.email)  # recipient=openai -> SUSPECTED


def declared_domestic(user: User):
    stripe.customers.create(email=user.pan)   # recipient=stripe; data_residency stripe=IN -> resolved_domestic


def domestic_hq_vendor(user: User):
    razorpay.customer.create(data={"contact": user.pan})   # recipient=razorpay (India HQ) -> not_suspected


def unknown_recipient(user: User):
    api_client.post("https://vendor.example/x", json={"email": user.email})  # unknown -> not_asserted
