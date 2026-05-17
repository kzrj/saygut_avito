from dataclasses import dataclass, field


@dataclass
class AuthIdentity:
    provider: str
    external_id: str
    meta: dict = field(default_factory=dict)
