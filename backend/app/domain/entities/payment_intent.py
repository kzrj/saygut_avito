from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class PaymentIntent:
    id: str
    user_id: str
    provider: str
    amount_rub: int
    coins_amount: int
    status: str
    external_payment_id: str | None
    confirmation_url: str | None
    transaction_id: str | None
    raw_webhook: dict[str, Any]
    created_at: datetime
    updated_at: datetime
