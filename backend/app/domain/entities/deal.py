from dataclasses import dataclass
from datetime import datetime


@dataclass
class Deal:
    """Reserved for escrow (Stage 8+)."""

    id: str
    listing_id: str
    buyer_id: str
    seller_id: str
    amount_coins: int
    status: str
    freeze_tx_id: str | None
    dispute_reason: str | None
    resolved_by: str | None
    created_at: datetime
