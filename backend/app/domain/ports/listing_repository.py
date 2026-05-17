from abc import ABC, abstractmethod

from app.domain.entities.listing import Listing


class ListingRepository(ABC):
    @abstractmethod
    async def get_by_id(self, listing_id: str) -> Listing | None: ...

    @abstractmethod
    async def save(self, listing: Listing) -> Listing: ...

    @abstractmethod
    async def list_catalog(
        self,
        *,
        page: int,
        limit: int,
        category_id: str | None = None,
        q: str | None = None,
    ) -> tuple[list[Listing], int]: ...

    @abstractmethod
    async def list_by_seller(
        self,
        seller_id: str,
        *,
        status: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Listing], int]: ...
