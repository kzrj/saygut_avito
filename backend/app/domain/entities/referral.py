from dataclasses import dataclass
from datetime import datetime


@dataclass
class Referral:
    id: str
    referrer_id: str
    referred_user_id: str
    status: str
    bonus_transaction_id: str | None
    created_at: datetime
