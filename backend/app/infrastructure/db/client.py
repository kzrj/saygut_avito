from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.infrastructure.db.documents.category_doc import CategoryDoc
from app.infrastructure.db.documents.listing_doc import ListingDoc
from app.infrastructure.db.documents.payment_intent_doc import PaymentIntentDoc
from app.infrastructure.db.documents.referral_doc import ReferralDoc
from app.infrastructure.db.documents.transaction_doc import TransactionDoc
from app.infrastructure.db.documents.user_doc import UserDoc

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    if _client is None:
        raise RuntimeError("Database not initialized")
    return _client


async def init_db() -> None:
    global _client
    _client = AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(
        database=_client[settings.mongodb_db],
        document_models=[
            UserDoc,
            ListingDoc,
            TransactionDoc,
            PaymentIntentDoc,
            ReferralDoc,
            CategoryDoc,
        ],
    )


async def close_db() -> None:
    global _client
    if _client:
        _client.close()
        _client = None
