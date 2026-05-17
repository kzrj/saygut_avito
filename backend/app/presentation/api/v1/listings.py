from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.domain.entities.listing import Listing
from app.domain.entities.user import User
from app.domain.exceptions import DomainError
from app.presentation.container import container
from app.presentation.deps import get_current_user
from app.presentation.schemas.listings import (
    CategoryItem,
    CreateListingRequest,
    ListingListResponse,
    ListingPublic,
    UpdateListingRequest,
)

router = APIRouter(prefix="/listings", tags=["listings"])


def _listing_public(l: Listing) -> ListingPublic:
    return ListingPublic(
        id=l.id,
        seller_id=l.seller_id,
        title=l.title,
        description=l.description,
        category_id=l.category_id,
        images=l.images,
        price_coins=l.price_coins,
        price_mode=l.price_mode,
        status=l.status,
        created_at=l.created_at,
        published_at=l.published_at,
    )


@router.get("/categories", response_model=list[CategoryItem])
async def categories():
    cats = await container.categories.list_all()
    return [CategoryItem(id=c.id, slug=c.slug, name=c.name) for c in cats]


@router.get("", response_model=ListingListResponse)
async def catalog(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = None,
    q: str | None = None,
):
    items, total = await container.list_catalog.execute(
        page=page, limit=limit, category_id=category, q=q
    )
    return ListingListResponse(
        items=[_listing_public(i) for i in items],
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/mine", response_model=ListingListResponse)
async def mine(
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = None,
):
    items, total = await container.listings.list_by_seller(
        user.id, status=status, page=page, limit=limit
    )
    return ListingListResponse(
        items=[_listing_public(i) for i in items],
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/{listing_id}", response_model=ListingPublic)
async def get_listing(listing_id: str):
    listing = await container.listings.get_by_id(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return _listing_public(listing)


@router.post("", response_model=ListingPublic)
async def create_listing(
    body: CreateListingRequest,
    user: User = Depends(get_current_user),
):
    try:
        listing = await container.create_listing.execute(
            user.id,
            title=body.title,
            description=body.description,
            price_coins=body.price_coins,
            images=body.images,
            category_id=body.category_id,
        )
    except DomainError as e:
        raise _http_from_domain(e) from e
    return _listing_public(listing)


@router.patch("/{listing_id}", response_model=ListingPublic)
async def update_listing(
    listing_id: str,
    body: UpdateListingRequest,
    user: User = Depends(get_current_user),
):
    try:
        listing = await container.update_listing.execute(
            user.id,
            listing_id,
            title=body.title,
            description=body.description,
            price_coins=body.price_coins,
            category_id=body.category_id,
            images=body.images,
        )
    except DomainError as e:
        raise _http_from_domain(e) from e
    return _listing_public(listing)


@router.post("/{listing_id}/publish", response_model=ListingPublic)
async def publish_listing(
    listing_id: str,
    user: User = Depends(get_current_user),
):
    try:
        listing = await container.publish_listing.execute(user.id, listing_id)
    except DomainError as e:
        raise _http_from_domain(e) from e
    return _listing_public(listing)


@router.post("/{listing_id}/archive", response_model=ListingPublic)
async def archive_listing(
    listing_id: str,
    user: User = Depends(get_current_user),
):
    try:
        listing = await container.archive_listing.execute(user.id, listing_id)
    except DomainError as e:
        raise _http_from_domain(e) from e
    return _listing_public(listing)


@router.post("/{listing_id}/images")
async def upload_images(
    listing_id: str,
    user: User = Depends(get_current_user),
    files: list[UploadFile] = File(...),
):
    listing = await container.listings.get_by_id(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Not your listing")
    urls = list(listing.images)
    for f in files:
        data = await f.read()
        url = await container.storage.save_image(data, f.filename or "image.jpg")
        urls.append(url)
    listing.images = urls
    saved = await container.listings.save(listing)
    return {"urls": saved.images}


def _http_from_domain(e: DomainError) -> HTTPException:
    codes = {
        "not_found": 404,
        "forbidden": 403,
        "insufficient_funds": 402,
        "conflict": 409,
        "validation_error": 400,
    }
    return HTTPException(status_code=codes.get(e.code, 400), detail=e.message)
