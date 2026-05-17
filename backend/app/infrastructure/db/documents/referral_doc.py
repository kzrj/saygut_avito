from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field


class ReferralDoc(Document):
    referrer_id: str
    referred_user_id: Indexed(str, unique=True)
    status: str = "pending"
    bonus_transaction_id: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "referrals"
