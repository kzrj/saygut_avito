from enum import StrEnum


class TransactionType(StrEnum):
    TOPUP = "topup"
    LISTING_FEE = "listing_fee"
    REFERRAL_BONUS = "referral_bonus"
    ADMIN_ADJUSTMENT = "admin_adjustment"
    ESCROW_FREEZE = "escrow_freeze"
    ESCROW_RELEASE = "escrow_release"
    ESCROW_REFUND = "escrow_refund"
    BARTER_BUYOUT = "barter_buyout"
    BARTER_PURCHASE = "barter_purchase"
    SUBSCRIPTION_PURCHASE = "subscription_purchase"
    AUCTION_BID_HOLD = "auction_bid_hold"
    AUCTION_WIN = "auction_win"
    PENALTY = "penalty"
