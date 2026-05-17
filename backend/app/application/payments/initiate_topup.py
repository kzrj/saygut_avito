import uuid
from datetime import datetime

from app.config import settings
from app.domain.entities.payment_intent import PaymentIntent
from app.domain.enums.payment_status import PaymentIntentStatus
from app.domain.exceptions import ValidationError
from app.domain.ports.payment_intent_repository import PaymentIntentRepository
from app.infrastructure.payments.provider_registry import PaymentProviderRegistry


class InitiateTopup:
    def __init__(
        self,
        intents: PaymentIntentRepository,
        providers: PaymentProviderRegistry,
    ) -> None:
        self._intents = intents
        self._providers = providers

    async def execute(
        self,
        user_id: str,
        *,
        amount_rub: int | None = None,
        coins_amount: int | None = None,
    ) -> PaymentIntent:
        if amount_rub is None and coins_amount is None:
            raise ValidationError("amount_rub or coins_amount required")

        if coins_amount is None:
            coins_amount = amount_rub // settings.rub_per_coin
        if amount_rub is None:
            amount_rub = coins_amount * settings.rub_per_coin

        if amount_rub <= 0 or coins_amount <= 0:
            raise ValidationError("Amount must be positive")

        provider = self._providers.get("yoomoney")
        now = datetime.utcnow()
        intent = PaymentIntent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            provider=provider.provider_id,
            amount_rub=amount_rub,
            coins_amount=coins_amount,
            status=PaymentIntentStatus.CREATED,
            external_payment_id=None,
            confirmation_url=None,
            transaction_id=None,
            raw_webhook={},
            created_at=now,
            updated_at=now,
        )
        intent = await self._intents.save(intent)

        result = await provider.create_payment(
            amount_rub=amount_rub,
            description=f"MicroAvito top-up {coins_amount} coins",
            return_url=settings.yoomoney_return_url,
            metadata={"intent_id": intent.id, "user_id": user_id},
        )

        intent.external_payment_id = result.external_payment_id
        intent.confirmation_url = result.confirmation_url
        intent.status = PaymentIntentStatus.PENDING
        return await self._intents.save(intent)
