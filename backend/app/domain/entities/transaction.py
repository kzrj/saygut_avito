from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.domain.value_objects.entity_ref import EntityRef


@dataclass
class Transaction:
    id: str
    user_id: str
    type: str
    amount: int
    balance_after: int
    status: str
    related: EntityRef | None
    idempotency_key: str | None
    payment_provider: str | None
    external_id: str | None
    metadata: dict[str, Any]
    created_at: datetime
