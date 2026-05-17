from datetime import datetime

from pydantic import BaseModel, Field


class CreateListingRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    price_coins: int = Field(gt=0)
    images: list[str] = []
    category_id: str | None = None


class UpdateListingRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price_coins: int | None = Field(default=None, gt=0)
    images: list[str] | None = None
    category_id: str | None = None


class ListingPublic(BaseModel):
    id: str
    seller_id: str
    title: str
    description: str
    category_id: str | None
    images: list[str]
    price_coins: int
    price_mode: str
    status: str
    created_at: datetime
    published_at: datetime | None


class ListingListResponse(BaseModel):
    items: list[ListingPublic]
    page: int
    limit: int
    total: int


class CategoryItem(BaseModel):
    id: str
    slug: str
    name: str
