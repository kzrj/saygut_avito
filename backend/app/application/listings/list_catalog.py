from app.domain.entities.listing import Listing
from app.domain.ports.listing_repository import ListingRepository


class ListCatalog:
    def __init__(self, listings: ListingRepository) -> None:
        self._listings = listings

    async def execute(
        self,
        *,
        page: int = 1,
        limit: int = 20,
        category_id: str | None = None,
        q: str | None = None,
    ) -> tuple[list[Listing], int]:
        return await self._listings.list_catalog(
            page=page, limit=limit, category_id=category_id, q=q
        )
