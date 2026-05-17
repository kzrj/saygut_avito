from enum import StrEnum


class PaymentIntentStatus(StrEnum):
    CREATED = "created"
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    EXPIRED = "expired"


class TransactionStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"


class ReferralStatus(StrEnum):
    PENDING = "pending"
    REWARDED = "rewarded"
    REJECTED = "rejected"
