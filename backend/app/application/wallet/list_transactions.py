from app.domain.entities.transaction import Transaction
from app.domain.ports.transaction_repository import TransactionRepository


class ListTransactions:
    def __init__(self, transactions: TransactionRepository) -> None:
        self._transactions = transactions

    async def execute(
        self,
        user_id: str,
        *,
        page: int = 1,
        limit: int = 20,
        tx_type: str | None = None,
    ) -> tuple[list[Transaction], int]:
        return await self._transactions.list_by_user(
            user_id, page=page, limit=limit, tx_type=tx_type
        )
