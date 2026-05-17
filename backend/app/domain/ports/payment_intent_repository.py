from abc import ABC, abstractmethod

from app.domain.entities.payment_intent import PaymentIntent


class PaymentIntentRepository(ABC):
    @abstractmethod
    async def get_by_id(self, intent_id: str) -> PaymentIntent | None: ...

    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> PaymentIntent | None: ...

    @abstractmethod
    async def save(self, intent: PaymentIntent) -> PaymentIntent: ...
