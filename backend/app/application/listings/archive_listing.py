from app.domain.entities.listing import Listing
from app.domain.enums.listing_status import ListingStatus
from app.domain.exceptions import ForbiddenError, NotFoundError
from app.domain.ports.listing_repository import ListingRepository


class ArchiveListing:
    def __init__(self, listings: ListingRepository) -> None:
        self._listings = listings

    async def execute(self, seller_id: str, listing_id: str) -> Listing:
        listing = await self._listings.get_by_id(listing_id)
        if not listing:
            raise NotFoundError("Listing not found")
        if listing.seller_id != seller_id:
            raise ForbiddenError("Not your listing")
        listing.status = ListingStatus.ARCHIVED
        return await self._listings.save(listing)
