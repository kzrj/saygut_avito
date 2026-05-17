from datetime import datetime

from beanie import PydanticObjectId

from app.domain.entities.transaction import Transaction
from app.domain.enums.payment_status import TransactionStatus
from app.domain.enums.transaction_type import TransactionType
from app.domain.exceptions import InsufficientFundsError
from app.domain.ports.transaction_repository import TransactionRepository
from app.domain.ports.user_repository import UserRepository
from app.domain.value_objects.entity_ref import EntityRef
from app.infrastructure.db.documents.transaction_doc import RelatedEmbedded, TransactionDoc
from app.infrastructure.db.documents.user_doc import UserDoc
from app.infrastructure.db.mappers import transaction_to_entity


class PostLedgerEntry:
    def __init__(
        self,
        users: UserRepository,
        transactions: TransactionRepository,
    ) -> None:
        self._users = users
        self._transactions = transactions

    async def execute(
        self,
        *,
        user_id: str,
        tx_type: TransactionType | str,
        amount: int,
        related: EntityRef | None = None,
        idempotency_key: str | None = None,
        payment_provider: str | None = None,
        external_id: str | None = None,
        metadata: dict | None = None,
        status: str = TransactionStatus.COMPLETED,
    ) -> Transaction:
        if idempotency_key:
            existing = await self._transactions.get_by_idempotency_key(idempotency_key)
            if existing:
                return existing

        user_doc = await UserDoc.get(PydanticObjectId(user_id))
        if not user_doc:
            raise InsufficientFundsError("User not found")

        new_balance = user_doc.wallet_balance + amount
        if new_balance < 0:
            raise InsufficientFundsError("Insufficient coins")

        user_doc.wallet_balance = new_balance
        user_doc.updated_at = datetime.utcnow()
        await user_doc.save()

        tx_doc = TransactionDoc(
            user_id=user_id,
            type=str(tx_type),
            amount=amount,
            balance_after=new_balance,
            status=status,
            related=(
                RelatedEmbedded(
                    entity_type=related.entity_type,
                    entity_id=related.entity_id,
                )
                if related
                else None
            ),
            idempotency_key=idempotency_key,
            payment_provider=payment_provider,
            external_id=external_id,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
        )
        await tx_doc.insert()

        return transaction_to_entity(tx_doc)
