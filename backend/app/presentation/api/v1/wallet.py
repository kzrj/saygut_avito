from fastapi import APIRouter, Depends, HTTPException, Query

from app.config import settings
from app.domain.entities.user import User
from app.domain.enums.transaction_type import TransactionType
from app.domain.exceptions import DomainError
from app.presentation.container import container
from app.presentation.deps import get_current_user
from app.presentation.schemas.wallet import (
    AdminCreditRequest,
    BalanceResponse,
    TransactionItem,
    TransactionListResponse,
)

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/balance", response_model=BalanceResponse)
async def balance(user: User = Depends(get_current_user)):
    bal = await container.get_balance.execute(user.id)
    return BalanceResponse(balance=bal)


@router.get("/transactions", response_model=TransactionListResponse)
async def transactions(
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    type: str | None = None,
):
    items, total = await container.list_transactions.execute(
        user.id, page=page, limit=limit, tx_type=type
    )
    return TransactionListResponse(
        items=[
            TransactionItem(
                id=t.id,
                type=t.type,
                amount=t.amount,
                balance_after=t.balance_after,
                status=t.status,
                related_type=t.related.entity_type if t.related else None,
                related_id=t.related.entity_id if t.related else None,
                created_at=t.created_at,
            )
            for t in items
        ],
        page=page,
        limit=limit,
        total=total,
    )


@router.post("/admin/credit", response_model=BalanceResponse)
async def admin_credit(
    body: AdminCreditRequest,
    user: User = Depends(get_current_user),
):
    if not settings.enable_admin_credit:
        raise HTTPException(status_code=403, detail="Admin credit disabled")
    try:
        await container.ledger.execute(
            user_id=user.id,
            tx_type=TransactionType.ADMIN_ADJUSTMENT,
            amount=body.amount,
        )
    except DomainError as e:
        raise HTTPException(status_code=400, detail=e.message) from e
    bal = await container.get_balance.execute(user.id)
    return BalanceResponse(balance=bal)
