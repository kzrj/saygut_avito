import json
import uuid
from typing import Any

from app.config import settings
from app.domain.ports.payment_provider import (
    PaymentCreateResult,
    PaymentProvider,
    WebhookParseResult,
)


class MockYooMoneyProvider(PaymentProvider):
    """Used when YOOMONEY credentials are not configured (local dev)."""

    provider_id = "yoomoney"

    async def create_payment(
        self,
        *,
        amount_rub: int,
        description: str,
        return_url: str,
        metadata: dict[str, Any],
    ) -> PaymentCreateResult:
        payment_id = f"mock_{uuid.uuid4().hex[:12]}"
        base = settings.app_public_url.rstrip("/")
        confirmation_url = (
            f"{base}/api/v1/payments/mock-confirm"
            f"?payment_id={payment_id}&return_url={return_url}"
        )
        return PaymentCreateResult(
            external_payment_id=payment_id,
            confirmation_url=confirmation_url,
        )

    def verify_webhook(self, body: bytes, headers: dict[str, str]) -> bool:
        return True

    def parse_webhook(self, body: bytes) -> WebhookParseResult:
        data = json.loads(body)
        return WebhookParseResult(
            external_payment_id=data["external_payment_id"],
            status=data.get("status", "succeeded"),
            raw=data,
        )
