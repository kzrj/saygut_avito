from abc import ABC, abstractmethod

from app.domain.entities.referral import Referral


class ReferralRepository(ABC):
    @abstractmethod
    async def save(self, referral: Referral) -> Referral: ...

    @abstractmethod
    async def get_by_referred_user(self, referred_user_id: str) -> Referral | None: ...

    @abstractmethod
    async def count_by_referrer(self, referrer_id: str) -> int: ...

    @abstractmethod
    async def sum_earned_by_referrer(self, referrer_id: str) -> int: ...
