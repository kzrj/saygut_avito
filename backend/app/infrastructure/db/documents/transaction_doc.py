from datetime import datetime
from typing import Any, Optional

from beanie import Document, Indexed
from pydantic import BaseModel, Field


class RelatedEmbedded(BaseModel):
    entity_type: str
    entity_id: str


class TransactionDoc(Document):
    user_id: Indexed(str)
    type: str
    amount: int
    balance_after: int
    status: str = "completed"
    related: RelatedEmbedded | None = None
    idempotency_key: Optional[str] = None
    payment_provider: Optional[str] = None
    external_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "transactions"
        indexes = [
            [("user_id", 1), ("created_at", -1)],
            [("idempotency_key", 1)],
        ]
