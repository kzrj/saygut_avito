from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Listing:
    id: str
    seller_id: str
    title: str
    description: str
    category_id: str | None
    images: list[str]
    price_coins: int
    price_mode: str
    status: str
    auction: dict[str, Any] | None
    listing_fee_tx_id: str | None
    reserved_for_deal_id: str | None
    metadata: dict[str, Any]
    created_at: datetime
    published_at: datetime | None
    sold_at: datetime | None
