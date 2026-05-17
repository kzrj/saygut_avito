import json
from datetime import datetime

from app.domain.enums.payment_status import PaymentIntentStatus
from app.domain.exceptions import NotFoundError, ValidationError
from app.domain.ports.payment_intent_repository import PaymentIntentRepository
from app.application.payments.handle_webhook import HandleWebhook


class ConfirmMockPayment:
    def __init__(
        self,
        intents: PaymentIntentRepository,
        webhook: HandleWebhook,
    ) -> None:
        self._intents = intents
        self._webhook = webhook

    async def execute(self, external_payment_id: str) -> None:
        intent = await self._intents.get_by_external_id(external_payment_id)
        if not intent:
            raise NotFoundError("Payment not found")
        if intent.status == PaymentIntentStatus.SUCCEEDED:
            return

        body = json.dumps(
            {"external_payment_id": external_payment_id, "status": "succeeded"}
        ).encode()
        await self._webhook.execute("yoomoney", body, {})
