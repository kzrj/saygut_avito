from beanie import PydanticObjectId

from app.domain.entities.referral import Referral
from app.domain.enums.payment_status import ReferralStatus
from app.domain.enums.transaction_type import TransactionType
from app.domain.ports.referral_repository import ReferralRepository
from app.infrastructure.db.documents.referral_doc import ReferralDoc
from app.infrastructure.db.documents.transaction_doc import TransactionDoc
from app.infrastructure.db.mappers import referral_to_entity


class MongoReferralRepository(ReferralRepository):
    async def save(self, referral: Referral) -> Referral:
        if referral.id:
            doc = await ReferralDoc.get(PydanticObjectId(referral.id))
            if doc:
                doc.status = referral.status
                doc.bonus_transaction_id = referral.bonus_transaction_id
                await doc.save()
                return referral_to_entity(doc)
        doc = ReferralDoc(
            referrer_id=referral.referrer_id,
            referred_user_id=referral.referred_user_id,
            status=referral.status,
            bonus_transaction_id=referral.bonus_transaction_id,
            created_at=referral.created_at,
        )
        await doc.insert()
        return referral_to_entity(doc)

    async def get_by_referred_user(self, referred_user_id: str) -> Referral | None:
        doc = await ReferralDoc.find_one(
            ReferralDoc.referred_user_id == referred_user_id
        )
        return referral_to_entity(doc) if doc else None

    async def count_by_referrer(self, referrer_id: str) -> int:
        return await ReferralDoc.find(ReferralDoc.referrer_id == referrer_id).count()

    async def sum_earned_by_referrer(self, referrer_id: str) -> int:
        pipeline = [
            {"$match": {"referrer_id": referrer_id, "status": ReferralStatus.REWARDED}},
        ]
        referrals = await ReferralDoc.find(
            ReferralDoc.referrer_id == referrer_id,
            ReferralDoc.status == ReferralStatus.REWARDED,
        ).to_list()
        total = 0
        for ref in referrals:
            if ref.bonus_transaction_id:
                tx = await TransactionDoc.get(
                    PydanticObjectId(ref.bonus_transaction_id)
                )
                if tx and tx.type == TransactionType.REFERRAL_BONUS:
                    total += tx.amount
        return total
