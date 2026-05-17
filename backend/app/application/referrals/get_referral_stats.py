from app.config import settings
from app.domain.ports.referral_repository import ReferralRepository
from app.domain.ports.user_repository import UserRepository


class ReferralStats:
    code: str
    invited_count: int
    earned_coins: int
    link: str


class GetReferralStats:
    def __init__(
        self,
        users: UserRepository,
        referrals: ReferralRepository,
    ) -> None:
        self._users = users
        self._referrals = referrals

    async def execute(self, user_id: str) -> ReferralStats:
        user = await self._users.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        invited = await self._referrals.count_by_referrer(user_id)
        earned = await self._referrals.sum_earned_by_referrer(user_id)
        base = settings.app_public_url.rstrip("/")
        return ReferralStats(
            code=user.referral_code,
            invited_count=invited,
            earned_coins=earned,
            link=f"{base}/register?ref={user.referral_code}",
        )
