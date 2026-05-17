from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import BaseModel, Field
from pymongo import ASCENDING, IndexModel


class IdentityEmbedded(BaseModel):
    provider: str
    external_id: str
    meta: dict = Field(default_factory=dict)


class UserDoc(Document):
    email: Optional[str] = None
    phone: Optional[str] = None
    password_hash: Optional[str] = None
    display_name: str = ""
    wallet_balance: int = 0
    referral_code: Indexed(str, unique=True)
    referred_by_id: Optional[str] = None
    identities: list[IdentityEmbedded] = Field(default_factory=list)
    role: str = "user"
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True, sparse=True),
            IndexModel([("phone", ASCENDING)], unique=True, sparse=True),
        ]
