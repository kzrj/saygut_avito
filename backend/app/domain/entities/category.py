from dataclasses import dataclass


@dataclass
class Category:
    id: str
    slug: str
    name: str
