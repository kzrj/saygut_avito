from datetime import datetime

from beanie import PydanticObjectId

from app.domain.entities.payment_intent import PaymentIntent
from app.domain.ports.payment_intent_repository import PaymentIntentRepository
from app.infrastructure.db.documents.payment_intent_doc import PaymentIntentDoc
from app.infrastructure.db.mappers import payment_intent_to_entity


class MongoPaymentIntentRepository(PaymentIntentRepository):
    async def get_by_id(self, intent_id: str) -> PaymentIntent | None:
        doc = await PaymentIntentDoc.get(PydanticObjectId(intent_id))
        return payment_intent_to_entity(doc) if doc else None

    async def get_by_external_id(self, external_id: str) -> PaymentIntent | None:
        doc = await PaymentIntentDoc.find_one(
            PaymentIntentDoc.external_payment_id == external_id
        )
        return payment_intent_to_entity(doc) if doc else None

    async def save(self, intent: PaymentIntent) -> PaymentIntent:
        oid = PydanticObjectId(intent.id) if intent.id else None
        if oid:
            doc = await PaymentIntentDoc.get(oid)
            if not doc:
                doc = PaymentIntentDoc(id=oid)
        else:
            doc = PaymentIntentDoc()

        doc.user_id = intent.user_id
        doc.provider = intent.provider
        doc.amount_rub = intent.amount_rub
        doc.coins_amount = intent.coins_amount
        doc.status = intent.status
        doc.external_payment_id = intent.external_payment_id
        doc.confirmation_url = intent.confirmation_url
        doc.transaction_id = intent.transaction_id
        doc.raw_webhook = intent.raw_webhook
        doc.updated_at = datetime.utcnow()
        if not doc.created_at:
            doc.created_at = intent.created_at
        await doc.save()
        return payment_intent_to_entity(doc)
