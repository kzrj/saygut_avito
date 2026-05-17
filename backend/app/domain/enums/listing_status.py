from enum import StrEnum


class ListingStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    RESERVED = "reserved"
    SOLD = "sold"
    ARCHIVED = "archived"
