from datetime import datetime

from app.domain.entities.referral import Referral
from app.domain.enums.payment_status import ReferralStatus
from app.domain.exceptions import NotFoundError, ValidationError
from app.domain.ports.referral_repository import ReferralRepository
from app.domain.ports.user_repository import UserRepository


class ApplyReferral:
    def __init__(
        self,
        users: UserRepository,
        referrals: ReferralRepository,
    ) -> None:
        self._users = users
        self._referrals = referrals

    async def on_register(self, new_user_id: str, referral_code: str) -> None:
        referrer = await self._users.get_by_referral_code(referral_code.strip())
        if not referrer:
            raise ValidationError("Invalid referral code")
        if referrer.id == new_user_id:
            raise ValidationError("Cannot use your own referral code")

        existing = await self._referrals.get_by_referred_user(new_user_id)
        if existing:
            return

        user = await self._users.get_by_id(new_user_id)
        if not user:
            raise NotFoundError("User not found")
        user.referred_by_id = referrer.id
        await self._users.save(user)

        referral = Referral(
            id="",
            referrer_id=referrer.id,
            referred_user_id=new_user_id,
            status=ReferralStatus.PENDING,
            bonus_transaction_id=None,
            created_at=datetime.utcnow(),
        )
        await self._referrals.save(referral)
