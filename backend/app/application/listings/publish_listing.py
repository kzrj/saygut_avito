from datetime import datetime

from app.config import settings
from app.domain.entities.listing import Listing
from app.domain.enums.listing_status import ListingStatus
from app.domain.enums.transaction_type import TransactionType
from app.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.domain.ports.listing_repository import ListingRepository
from app.domain.value_objects.entity_ref import EntityRef
from app.application.wallet.post_ledger_entry import PostLedgerEntry
from app.application.referrals.reward_referral import RewardReferral


class PublishListing:
    def __init__(
        self,
        listings: ListingRepository,
        ledger: PostLedgerEntry,
        reward_referral: RewardReferral,
    ) -> None:
        self._listings = listings
        self._ledger = ledger
        self._reward_referral = reward_referral

    async def execute(self, seller_id: str, listing_id: str) -> Listing:
        listing = await self._listings.get_by_id(listing_id)
        if not listing:
            raise NotFoundError("Listing not found")
        if listing.seller_id != seller_id:
            raise ForbiddenError("Not your listing")
        if listing.status != ListingStatus.DRAFT:
            raise ValidationError("Only draft listings can be published")

        fee = settings.listing_fee_coins
        tx = await self._ledger.execute(
            user_id=seller_id,
            tx_type=TransactionType.LISTING_FEE,
            amount=-fee,
            related=EntityRef("listing", listing_id),
        )

        listing.status = ListingStatus.ACTIVE
        listing.listing_fee_tx_id = tx.id
        listing.published_at = datetime.utcnow()
        saved = await self._listings.save(listing)

        await self._reward_referral.on_first_publish(seller_id)
        return saved
