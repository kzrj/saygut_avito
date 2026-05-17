from dataclasses import dataclass
from datetime import datetime


@dataclass
class Subscription:
    """Reserved for seller packages (Stage 9+)."""

    id: str
    user_id: str
    plan_code: str
    listings_quota: int
    listings_used: int
    expires_at: datetime
    purchase_tx_id: str | None
