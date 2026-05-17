from datetime import datetime
from typing import Any

from beanie import Document
from pydantic import Field


class PaymentIntentDoc(Document):
    user_id: str
    provider: str
    amount_rub: int
    coins_amount: int
    status: str = "created"
    external_payment_id: str | None = None
    confirmation_url: str | None = None
    transaction_id: str | None = None
    raw_webhook: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "payment_intents"
