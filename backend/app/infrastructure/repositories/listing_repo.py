import re

from beanie import PydanticObjectId

from app.domain.entities.listing import Listing
from app.domain.enums.listing_status import ListingStatus
from app.domain.ports.listing_repository import ListingRepository
from app.infrastructure.db.documents.listing_doc import ListingDoc
from app.infrastructure.db.mappers import listing_to_entity


class MongoListingRepository(ListingRepository):
    def _listing_fields(self, listing: Listing) -> dict:
        return {
            "seller_id": listing.seller_id,
            "title": listing.title,
            "description": listing.description,
            "category_id": listing.category_id,
            "images": listing.images,
            "price_coins": listing.price_coins,
            "price_mode": listing.price_mode,
            "status": listing.status,
            "auction": listing.auction,
            "listing_fee_tx_id": listing.listing_fee_tx_id,
            "reserved_for_deal_id": listing.reserved_for_deal_id,
            "metadata": listing.metadata,
            "created_at": listing.created_at,
            "published_at": listing.published_at,
            "sold_at": listing.sold_at,
        }

    async def get_by_id(self, listing_id: str) -> Listing | None:
        doc = await ListingDoc.get(PydanticObjectId(listing_id))
        return listing_to_entity(doc) if doc else None

    async def save(self, listing: Listing) -> Listing:
        doc = None
        if listing.id:
            try:
                doc = await ListingDoc.get(PydanticObjectId(listing.id))
            except Exception:
                doc = None

        if doc is None:
            doc = ListingDoc(**self._listing_fields(listing))
        else:
            for key, value in self._listing_fields(listing).items():
                setattr(doc, key, value)

        await doc.save()
        return listing_to_entity(doc)

    async def list_catalog(
        self,
        *,
        page: int,
        limit: int,
        category_id: str | None = None,
        q: str | None = None,
    ) -> tuple[list[Listing], int]:
        query = ListingDoc.find(ListingDoc.status == ListingStatus.ACTIVE)
        if category_id:
            query = query.find(ListingDoc.category_id == category_id)
        if q:
            regex = re.compile(re.escape(q), re.IGNORECASE)
            query = query.find(
                {
                    "$or": [
                        {"title": {"$regex": regex}},
                        {"description": {"$regex": regex}},
                    ]
                }
            )
        total = await query.count()
        docs = (
            await query.sort(-ListingDoc.published_at)
            .skip((page - 1) * limit)
            .limit(limit)
            .to_list()
        )
        return [listing_to_entity(d) for d in docs], total

    async def list_by_seller(
        self,
        seller_id: str,
        *,
        status: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Listing], int]:
        query = ListingDoc.find(ListingDoc.seller_id == seller_id)
        if status:
            query = query.find(ListingDoc.status == status)
        total = await query.count()
        docs = (
            await query.sort(-ListingDoc.created_at)
            .skip((page - 1) * limit)
            .limit(limit)
            .to_list()
        )
        return [listing_to_entity(d) for d in docs], total
