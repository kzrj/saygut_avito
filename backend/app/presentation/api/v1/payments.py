from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.domain.entities.user import User
from app.domain.exceptions import DomainError
from app.presentation.container import container
from app.presentation.deps import get_current_user
from app.presentation.schemas.payments import (
    PaymentStatusResponse,
    TopupRequest,
    TopupResponse,
)

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/topup", response_model=TopupResponse)
async def topup(body: TopupRequest, user: User = Depends(get_current_user)):
    try:
        intent = await container.initiate_topup.execute(
            user.id,
            amount_rub=body.amount_rub,
            coins_amount=body.coins_amount,
        )
    except DomainError as e:
        raise HTTPException(status_code=400, detail=e.message) from e
    return TopupResponse(
        payment_id=intent.id,
        confirmation_url=intent.confirmation_url or "",
    )


@router.get("/{payment_id}/status", response_model=PaymentStatusResponse)
async def payment_status(
    payment_id: str,
    user: User = Depends(get_current_user),
):
    intent = await container.payment_intents.get_by_id(payment_id)
    if not intent or intent.user_id != user.id:
        raise HTTPException(status_code=404, detail="Payment not found")
    return PaymentStatusResponse(
        id=intent.id,
        status=intent.status,
        amount_rub=intent.amount_rub,
        coins_amount=intent.coins_amount,
        confirmation_url=intent.confirmation_url,
        transaction_id=intent.transaction_id,
        created_at=intent.created_at,
    )


@router.post("/webhook/yoomoney")
async def yoomoney_webhook(request: Request):
    body = await request.body()
    headers = {k.lower(): v for k, v in request.headers.items()}
    try:
        await container.handle_webhook.execute("yoomoney", body, headers)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"ok": True}


@router.get("/mock-confirm")
async def mock_confirm(
    payment_id: str = Query(..., alias="payment_id"),
    return_url: str = Query(""),
):
    """Dev-only: confirm mock YooMoney payment and redirect back."""
    try:
        await container.confirm_mock_payment.execute(payment_id)
    except DomainError as e:
        raise HTTPException(status_code=404, detail=e.message) from e
    from fastapi.responses import RedirectResponse

    return RedirectResponse(url=return_url or "/wallet")
