from datetime import datetime
from typing import Any

from beanie import Document, Indexed
from pydantic import Field


class ListingDoc(Document):
    seller_id: Indexed(str)
    title: str
    description: str = ""
    category_id: str | None = None
    images: list[str] = Field(default_factory=list)
    price_coins: int
    price_mode: str = "fixed"
    status: Indexed(str) = "draft"
    auction: dict[str, Any] | None = None
    listing_fee_tx_id: str | None = None
    reserved_for_deal_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: datetime | None = None
    sold_at: datetime | None = None

    class Settings:
        name = "listings"
        indexes = [
            [("status", 1), ("published_at", -1)],
            [("seller_id", 1), ("status", 1)],
        ]
