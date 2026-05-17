from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass
class TokenPayload:
    sub: str
    type: str


class TokenService(ABC):
    @abstractmethod
    def create_tokens(self, user_id: str) -> TokenPair: ...

    @abstractmethod
    def decode_access(self, token: str) -> TokenPayload: ...

    @abstractmethod
    def decode_refresh(self, token: str) -> TokenPayload: ...

    @abstractmethod
    def refresh_tokens(self, refresh_token: str) -> TokenPair: ...
