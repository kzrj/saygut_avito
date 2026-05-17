from app.domain.entities.category import Category
from app.domain.ports.category_repository import CategoryRepository
from app.infrastructure.db.documents.category_doc import CategoryDoc
from app.infrastructure.db.mappers import category_to_entity

DEFAULT_CATEGORIES = [
    ("electronics", "Электроника"),
    ("clothing", "Одежда"),
    ("home", "Дом и сад"),
    ("services", "Услуги"),
    ("other", "Другое"),
]


class MongoCategoryRepository(CategoryRepository):
    async def list_all(self) -> list[Category]:
        docs = await CategoryDoc.find_all().sort("+name").to_list()
        return [category_to_entity(d) for d in docs]

    async def get_by_id(self, category_id: str) -> Category | None:
        from beanie import PydanticObjectId

        doc = await CategoryDoc.get(PydanticObjectId(category_id))
        return category_to_entity(doc) if doc else None

    async def seed_defaults(self) -> None:
        for slug, name in DEFAULT_CATEGORIES:
            existing = await CategoryDoc.find_one(CategoryDoc.slug == slug)
            if not existing:
                await CategoryDoc(slug=slug, name=name).insert()
