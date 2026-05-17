from app.domain.entities.category import Category
from app.domain.entities.listing import Listing
from app.domain.entities.payment_intent import PaymentIntent
from app.domain.entities.referral import Referral
from app.domain.entities.transaction import Transaction
from app.domain.entities.user import User
from app.domain.value_objects.auth_identity import AuthIdentity
from app.domain.value_objects.entity_ref import EntityRef
from app.infrastructure.db.documents.category_doc import CategoryDoc
from app.infrastructure.db.documents.listing_doc import ListingDoc
from app.infrastructure.db.documents.payment_intent_doc import PaymentIntentDoc
from app.infrastructure.db.documents.referral_doc import ReferralDoc
from app.infrastructure.db.documents.transaction_doc import TransactionDoc
from app.infrastructure.db.documents.user_doc import UserDoc


def user_to_entity(doc: UserDoc) -> User:
    return User(
        id=str(doc.id),
        email=doc.email,
        phone=doc.phone,
        display_name=doc.display_name,
        wallet_balance=doc.wallet_balance,
        referral_code=doc.referral_code,
        referred_by_id=doc.referred_by_id,
        identities=[
            AuthIdentity(i.provider, i.external_id, i.meta) for i in doc.identities
        ],
        role=doc.role,
        status=doc.status,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        password_hash=doc.password_hash,
    )


def listing_to_entity(doc: ListingDoc) -> Listing:
    return Listing(
        id=str(doc.id),
        seller_id=doc.seller_id,
        title=doc.title,
        description=doc.description,
        category_id=doc.category_id,
        images=doc.images,
        price_coins=doc.price_coins,
        price_mode=doc.price_mode,
        status=doc.status,
        auction=doc.auction,
        listing_fee_tx_id=doc.listing_fee_tx_id,
        reserved_for_deal_id=doc.reserved_for_deal_id,
        metadata=doc.metadata,
        created_at=doc.created_at,
        published_at=doc.published_at,
        sold_at=doc.sold_at,
    )


def transaction_to_entity(doc: TransactionDoc) -> Transaction:
    related = None
    if doc.related:
        related = EntityRef(doc.related.entity_type, doc.related.entity_id)
    return Transaction(
        id=str(doc.id),
        user_id=doc.user_id,
        type=doc.type,
        amount=doc.amount,
        balance_after=doc.balance_after,
        status=doc.status,
        related=related,
        idempotency_key=doc.idempotency_key,
        payment_provider=doc.payment_provider,
        external_id=doc.external_id,
        metadata=doc.metadata,
        created_at=doc.created_at,
    )


def payment_intent_to_entity(doc: PaymentIntentDoc) -> PaymentIntent:
    return PaymentIntent(
        id=str(doc.id),
        user_id=doc.user_id,
        provider=doc.provider,
        amount_rub=doc.amount_rub,
        coins_amount=doc.coins_amount,
        status=doc.status,
        external_payment_id=doc.external_payment_id,
        confirmation_url=doc.confirmation_url,
        transaction_id=doc.transaction_id,
        raw_webhook=doc.raw_webhook,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
    )


def referral_to_entity(doc: ReferralDoc) -> Referral:
    return Referral(
        id=str(doc.id),
        referrer_id=doc.referrer_id,
        referred_user_id=doc.referred_user_id,
        status=doc.status,
        bonus_transaction_id=doc.bonus_transaction_id,
        created_at=doc.created_at,
    )


def category_to_entity(doc: CategoryDoc) -> Category:
    return Category(id=str(doc.id), slug=doc.slug, name=doc.name)
