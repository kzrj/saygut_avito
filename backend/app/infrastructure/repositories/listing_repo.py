import re

from beanie import PydanticObjectId

from app.domain.entities.listing import Listing
from app.domain.enums.listing_status import ListingStatus
from app.domain.ports.listing_repository import ListingRepository
from app.infrastructure.db.documents.listing_doc import ListingDoc
from app.infrastructure.db.mappers import listing_to_entity


class MongoListingRepository(ListingRepository):
    async def get_by_id(self, listing_id: str) -> Listing | None:
        doc = await ListingDoc.get(PydanticObjectId(listing_id))
        return listing_to_entity(doc) if doc else None

    async def save(self, listing: Listing) -> Listing:
        oid = PydanticObjectId(listing.id) if listing.id else None
        if oid:
            doc = await ListingDoc.get(oid)
            if not doc:
                doc = ListingDoc(id=oid)
        else:
            doc = ListingDoc()

        doc.seller_id = listing.seller_id
        doc.title = listing.title
        doc.description = listing.description
        doc.category_id = listing.category_id
        doc.images = listing.images
        doc.price_coins = listing.price_coins
        doc.price_mode = listing.price_mode
        doc.status = listing.status
        doc.auction = listing.auction
        doc.listing_fee_tx_id = listing.listing_fee_tx_id
        doc.reserved_for_deal_id = listing.reserved_for_deal_id
        doc.metadata = listing.metadata
        doc.created_at = listing.created_at
        doc.published_at = listing.published_at
        doc.sold_at = listing.sold_at
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
