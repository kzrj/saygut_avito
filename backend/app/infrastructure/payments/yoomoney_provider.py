import json
import uuid
from typing import Any

import httpx

from app.config import settings
from app.domain.exceptions import ValidationError
from app.domain.ports.payment_provider import (
    PaymentCreateResult,
    PaymentProvider,
    WebhookParseResult,
)


class YooMoneyProvider(PaymentProvider):
    provider_id = "yoomoney"
    API_URL = "https://api.yookassa.ru/v3/payments"

    async def create_payment(
        self,
        *,
        amount_rub: int,
        description: str,
        return_url: str,
        metadata: dict[str, Any],
    ) -> PaymentCreateResult:
        if not settings.yoomoney_shop_id or not settings.yoomoney_secret:
            raise ValidationError("YooMoney is not configured")

        payload = {
            "amount": {"value": f"{amount_rub:.2f}", "currency": "RUB"},
            "confirmation": {"type": "redirect", "return_url": return_url},
            "capture": True,
            "description": description,
            "metadata": metadata,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.API_URL,
                json=payload,
                auth=(settings.yoomoney_shop_id, settings.yoomoney_secret),
                headers={"Idempotence-Key": str(uuid.uuid4())},
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()

        confirmation = data.get("confirmation", {})
        return PaymentCreateResult(
            external_payment_id=data["id"],
            confirmation_url=confirmation.get("confirmation_url", return_url),
        )

    def verify_webhook(self, body: bytes, headers: dict[str, str]) -> bool:
        return bool(body)

    def parse_webhook(self, body: bytes) -> WebhookParseResult:
        data = json.loads(body)
        event = data.get("object", data)
        status_map = {
            "succeeded": "succeeded",
            "canceled": "failed",
            "pending": "pending",
        }
        payment_status = event.get("status", "")
        return WebhookParseResult(
            external_payment_id=event.get("id", ""),
            status=status_map.get(payment_status, payment_status),
            raw=data,
        )
