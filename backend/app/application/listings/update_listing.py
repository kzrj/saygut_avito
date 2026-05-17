from app.domain.entities.listing import Listing
from app.domain.enums.listing_status import ListingStatus
from app.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.domain.ports.listing_repository import ListingRepository


class UpdateListing:
    def __init__(self, listings: ListingRepository) -> None:
        self._listings = listings

    async def execute(
        self,
        seller_id: str,
        listing_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
        price_coins: int | None = None,
        category_id: str | None = None,
        images: list[str] | None = None,
    ) -> Listing:
        listing = await self._listings.get_by_id(listing_id)
        if not listing:
            raise NotFoundError("Listing not found")
        if listing.seller_id != seller_id:
            raise ForbiddenError("Not your listing")
        if listing.status != ListingStatus.DRAFT:
            raise ValidationError("Only draft listings can be edited")

        if title is not None:
            listing.title = title.strip()
        if description is not None:
            listing.description = description.strip()
        if price_coins is not None:
            if price_coins <= 0:
                raise ValidationError("Price must be positive")
            listing.price_coins = price_coins
        if category_id is not None:
            listing.category_id = category_id or None
        if images is not None:
            listing.images = images
        return await self._listings.save(listing)
