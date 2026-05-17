from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    async def save_image(self, data: bytes, filename: str) -> str: ...
