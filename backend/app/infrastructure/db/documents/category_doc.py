from beanie import Document, Indexed


class CategoryDoc(Document):
    slug: Indexed(str, unique=True)
    name: str

    class Settings:
        name = "categories"
