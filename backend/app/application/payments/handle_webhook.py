from datetime import datetime

from app.domain.enums.payment_status import PaymentIntentStatus, TransactionStatus
from app.domain.enums.transaction_type import TransactionType
from app.domain.exceptions import NotFoundError
from app.domain.ports.payment_intent_repository import PaymentIntentRepository
from app.domain.value_objects.entity_ref import EntityRef
from app.application.wallet.post_ledger_entry import PostLedgerEntry
from app.infrastructure.payments.provider_registry import PaymentProviderRegistry


class HandleWebhook:
    def __init__(
        self,
        intents: PaymentIntentRepository,
        providers: PaymentProviderRegistry,
        ledger: PostLedgerEntry,
    ) -> None:
        self._intents = intents
        self._providers = providers
        self._ledger = ledger

    async def execute(
        self,
        provider_id: str,
        body: bytes,
        headers: dict[str, str],
    ) -> None:
        provider = self._providers.get(provider_id)
        if not provider.verify_webhook(body, headers):
            raise ValueError("Invalid webhook signature")

        parsed = provider.parse_webhook(body)
        if parsed.status != "succeeded":
            return

        intent = await self._intents.get_by_external_id(parsed.external_payment_id)
        if not intent:
            raise NotFoundError("Payment intent not found")
        if intent.status == PaymentIntentStatus.SUCCEEDED:
            return

        idempotency_key = f"topup:{intent.id}"
        tx = await self._ledger.execute(
            user_id=intent.user_id,
            tx_type=TransactionType.TOPUP,
            amount=intent.coins_amount,
            related=EntityRef("payment_intent", intent.id),
            idempotency_key=idempotency_key,
            payment_provider=provider_id,
            external_id=parsed.external_payment_id,
            metadata=parsed.raw,
        )

        intent.status = PaymentIntentStatus.SUCCEEDED
        intent.transaction_id = tx.id
        intent.raw_webhook = parsed.raw
        intent.updated_at = datetime.utcnow()
        await self._intents.save(intent)
