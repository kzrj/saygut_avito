from app.config import settings
from app.domain.enums.payment_status import ReferralStatus
from app.domain.enums.transaction_type import TransactionType
from app.domain.ports.referral_repository import ReferralRepository
from app.domain.value_objects.entity_ref import EntityRef
from app.application.wallet.post_ledger_entry import PostLedgerEntry


class RewardReferral:
    def __init__(
        self,
        referrals: ReferralRepository,
        ledger: PostLedgerEntry,
    ) -> None:
        self._referrals = referrals
        self._ledger = ledger

    async def on_first_publish(self, referred_user_id: str) -> None:
        if settings.referral_reward_on != "first_publish":
            return

        referral = await self._referrals.get_by_referred_user(referred_user_id)
        if not referral or referral.status != ReferralStatus.PENDING:
            return

        bonus = settings.referral_bonus_coins
        ref_entity = EntityRef("referral", referral.id)

        referrer_tx = await self._ledger.execute(
            user_id=referral.referrer_id,
            tx_type=TransactionType.REFERRAL_BONUS,
            amount=bonus,
            related=ref_entity,
            metadata={"role": "referrer"},
        )
        await self._ledger.execute(
            user_id=referred_user_id,
            tx_type=TransactionType.REFERRAL_BONUS,
            amount=bonus,
            related=ref_entity,
            metadata={"role": "referred"},
        )

        referral.status = ReferralStatus.REWARDED
        referral.bonus_transaction_id = referrer_tx.id
        await self._referrals.save(referral)
