from datetime import datetime

from pydantic import BaseModel, model_validator


class TopupRequest(BaseModel):
    amount_rub: int | None = None
    coins_amount: int | None = None

    @model_validator(mode="after")
    def require_amount(self) -> "TopupRequest":
        if self.amount_rub is None and self.coins_amount is None:
            raise ValueError("amount_rub or coins_amount required")
        return self


class TopupResponse(BaseModel):
    payment_id: str
    confirmation_url: str


class PaymentStatusResponse(BaseModel):
    id: str
    status: str
    amount_rub: int
    coins_amount: int
    confirmation_url: str | None
    transaction_id: str | None
    created_at: datetime
