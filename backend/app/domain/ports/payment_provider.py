from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class PaymentCreateResult:
    external_payment_id: str
    confirmation_url: str


@dataclass
class WebhookParseResult:
    external_payment_id: str
    status: str
    raw: dict[str, Any]


class PaymentProvider(ABC):
    @property
    @abstractmethod
    def provider_id(self) -> str: ...

    @abstractmethod
    async def create_payment(
        self,
        *,
        amount_rub: int,
        description: str,
        return_url: str,
        metadata: dict[str, Any],
    ) -> PaymentCreateResult: ...

    @abstractmethod
    def verify_webhook(self, body: bytes, headers: dict[str, str]) -> bool: ...

    @abstractmethod
    def parse_webhook(self, body: bytes) -> WebhookParseResult: ...
