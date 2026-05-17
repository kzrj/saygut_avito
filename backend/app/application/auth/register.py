from app.domain.entities.user import User
from app.domain.exceptions import NotFoundError, ValidationError
from app.domain.ports.auth_provider import AuthCredentials, AuthProvider
from app.domain.ports.token_service import TokenPair, TokenService
from app.domain.ports.user_repository import UserRepository
from app.application.referrals.apply_referral import ApplyReferral


class RegisterUser:
    def __init__(
        self,
        auth: AuthProvider,
        tokens: TokenService,
        users: UserRepository,
        apply_referral: ApplyReferral,
    ) -> None:
        self._auth = auth
        self._tokens = tokens
        self._users = users
        self._apply_referral = apply_referral

    async def execute(
        self,
        *,
        email: str | None,
        phone: str | None,
        password: str,
        display_name: str | None,
        referral_code: str | None,
    ) -> tuple[TokenPair, User]:
        if referral_code:
            code = referral_code.strip()
            referrer = await self._users.get_by_referral_code(code)
            if not referrer:
                raise ValidationError("Invalid referral code")

        credentials = AuthCredentials(email=email, phone=phone, password=password)
        user = await self._auth.register(
            credentials, display_name or (email or phone or "User")
        )
        if referral_code:
            await self._apply_referral.on_register(user.id, referral_code.strip())
            user = await self._users.get_by_id(user.id)
            if not user:
                raise NotFoundError("User not found after register")
        token_pair = self._tokens.create_tokens(user.id)
        return token_pair, user
