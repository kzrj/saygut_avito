from abc import ABC, abstractmethod

from app.domain.entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    async def list_all(self) -> list[Category]: ...

    @abstractmethod
    async def get_by_id(self, category_id: str) -> Category | None: ...

    @abstractmethod
    async def seed_defaults(self) -> None: ...
