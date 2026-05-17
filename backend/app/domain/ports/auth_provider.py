from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.user import User


@dataclass
class AuthCredentials:
    email: str | None = None
    phone: str | None = None
    password: str = ""


class AuthProvider(ABC):
    @property
    @abstractmethod
    def provider_id(self) -> str: ...

    @abstractmethod
    async def authenticate(self, credentials: AuthCredentials) -> User: ...

    @abstractmethod
    async def register(self, credentials: AuthCredentials, display_name: str) -> User: ...
