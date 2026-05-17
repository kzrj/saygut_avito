from beanie import PydanticObjectId

from app.domain.entities.transaction import Transaction
from app.domain.ports.transaction_repository import TransactionRepository
from app.domain.value_objects.entity_ref import EntityRef
from app.infrastructure.db.documents.transaction_doc import RelatedEmbedded, TransactionDoc
from app.infrastructure.db.mappers import transaction_to_entity


class MongoTransactionRepository(TransactionRepository):
    async def save(self, tx: Transaction) -> Transaction:
        doc = TransactionDoc(
            user_id=tx.user_id,
            type=tx.type,
            amount=tx.amount,
            balance_after=tx.balance_after,
            status=tx.status,
            related=(
                RelatedEmbedded(
                    entity_type=tx.related.entity_type,
                    entity_id=tx.related.entity_id,
                )
                if tx.related
                else None
            ),
            idempotency_key=tx.idempotency_key,
            payment_provider=tx.payment_provider,
            external_id=tx.external_id,
            metadata=tx.metadata,
            created_at=tx.created_at,
        )
        if tx.id:
            doc.id = PydanticObjectId(tx.id)
        await doc.insert()
        return transaction_to_entity(doc)

    async def get_by_idempotency_key(self, key: str) -> Transaction | None:
        doc = await TransactionDoc.find_one(TransactionDoc.idempotency_key == key)
        return transaction_to_entity(doc) if doc else None

    async def list_by_user(
        self,
        user_id: str,
        *,
        page: int,
        limit: int,
        tx_type: str | None = None,
    ) -> tuple[list[Transaction], int]:
        query = TransactionDoc.find(TransactionDoc.user_id == user_id)
        if tx_type:
            query = query.find(TransactionDoc.type == tx_type)
        total = await query.count()
        docs = (
            await query.sort(-TransactionDoc.created_at)
            .skip((page - 1) * limit)
            .limit(limit)
            .to_list()
        )
        return [transaction_to_entity(d) for d in docs], total
