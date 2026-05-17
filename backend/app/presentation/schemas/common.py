from pydantic import BaseModel, Field


class PaginatedMeta(BaseModel):
    page: int
    limit: int
    total: int


class ErrorResponse(BaseModel):
    code: str
    message: str
