from datetime import datetime

from pydantic import BaseModel


class BalanceResponse(BaseModel):
    balance: int


class TransactionItem(BaseModel):
    id: str
    type: str
    amount: int
    balance_after: int
    status: str
    related_type: str | None = None
    related_id: str | None = None
    created_at: datetime


class TransactionListResponse(BaseModel):
    items: list[TransactionItem]
    page: int
    limit: int
    total: int


class AdminCreditRequest(BaseModel):
    amount: int
