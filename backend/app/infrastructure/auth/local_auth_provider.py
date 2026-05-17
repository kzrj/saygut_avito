import secrets
import string
import uuid
from datetime import datetime

from app.domain.entities.user import User
from app.domain.exceptions import ConflictError, UnauthorizedError, ValidationError
from app.domain.ports.auth_provider import AuthCredentials, AuthProvider
from app.domain.ports.user_repository import UserRepository
from app.domain.value_objects.auth_identity import AuthIdentity
from app.infrastructure.auth.password_hasher import hash_password, verify_password


def _generate_referral_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(8))


class LocalAuthProvider(AuthProvider):
    provider_id = "local"

    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def authenticate(self, credentials: AuthCredentials) -> User:
        user = await self._find_by_login(credentials)
        if not user or not user.password_hash:
            raise UnauthorizedError("Invalid credentials")
        if not verify_password(credentials.password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")
        if user.status != "active":
            raise UnauthorizedError("Account is blocked")
        return user

    async def register(self, credentials: AuthCredentials, display_name: str) -> User:
        if not credentials.email and not credentials.phone:
            raise ValidationError("Email or phone is required")
        if len(credentials.password) < 6:
            raise ValidationError("Password must be at least 6 characters")

        if credentials.email:
            existing = await self._users.get_by_email(credentials.email)
            if existing:
                raise ConflictError("Email already registered")
        if credentials.phone:
            existing = await self._users.get_by_phone(credentials.phone)
            if existing:
                raise ConflictError("Phone already registered")

        now = datetime.utcnow()
        external_id = (credentials.email or credentials.phone or "").lower()
        user = User(
            id=str(uuid.uuid4()),
            email=credentials.email.lower() if credentials.email else None,
            phone=credentials.phone,
            display_name=display_name or external_id,
            wallet_balance=0,
            referral_code=_generate_referral_code(),
            referred_by_id=None,
            identities=[
                AuthIdentity(
                    provider=self.provider_id,
                    external_id=external_id,
                    meta={},
                )
            ],
            role="user",
            status="active",
            created_at=now,
            updated_at=now,
            password_hash=hash_password(credentials.password),
        )
        return await self._users.save(user)

    async def _find_by_login(self, credentials: AuthCredentials) -> User | None:
        if credentials.email:
            return await self._users.get_by_email(credentials.email)
        if credentials.phone:
            return await self._users.get_by_phone(credentials.phone)
        return None
