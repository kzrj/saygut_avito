from dataclasses import dataclass, field
from datetime import datetime

from app.domain.value_objects.auth_identity import AuthIdentity


@dataclass
class User:
    id: str
    email: str | None
    phone: str | None
    display_name: str
    wallet_balance: int
    referral_code: str
    referred_by_id: str | None
    identities: list[AuthIdentity]
    role: str
    status: str
    created_at: datetime
    updated_at: datetime
    password_hash: str | None = field(default=None, repr=False)
