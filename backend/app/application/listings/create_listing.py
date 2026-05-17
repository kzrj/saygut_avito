from datetime import datetime

from app.domain.entities.listing import Listing
from app.domain.enums.listing_status import ListingStatus
from app.domain.enums.price_mode import PriceMode
from app.domain.exceptions import NotFoundError, ValidationError
from app.domain.ports.category_repository import CategoryRepository
from app.domain.ports.listing_repository import ListingRepository


class CreateListing:
    def __init__(
        self,
        listings: ListingRepository,
        categories: CategoryRepository,
    ) -> None:
        self._listings = listings
        self._categories = categories

    async def execute(
        self,
        seller_id: str,
        *,
        title: str,
        description: str,
        price_coins: int,
        images: list[str],
        category_id: str | None,
    ) -> Listing:
        if not title.strip():
            raise ValidationError("Title is required")
        if price_coins <= 0:
            raise ValidationError("Price must be positive")
        if category_id:
            cat = await self._categories.get_by_id(category_id)
            if not cat:
                raise NotFoundError("Category not found")

        now = datetime.utcnow()
        listing = Listing(
            id="",
            seller_id=seller_id,
            title=title.strip(),
            description=description.strip(),
            category_id=category_id,
            images=images,
            price_coins=price_coins,
            price_mode=PriceMode.FIXED,
            status=ListingStatus.DRAFT,
            auction=None,
            listing_fee_tx_id=None,
            reserved_for_deal_id=None,
            metadata={},
            created_at=now,
            published_at=None,
            sold_at=None,
        )
        return await self._listings.save(listing)
