from abc import ABC, abstractmethod

from app.domain.entities.transaction import Transaction


class TransactionRepository(ABC):
    @abstractmethod
    async def save(self, tx: Transaction) -> Transaction: ...

    @abstractmethod
    async def get_by_idempotency_key(self, key: str) -> Transaction | None: ...

    @abstractmethod
    async def list_by_user(
        self,
        user_id: str,
        *,
        page: int,
        limit: int,
        tx_type: str | None = None,
    ) -> tuple[list[Transaction], int]: ...
