from app.domain.entities.user import User
from app.domain.ports.auth_provider import AuthCredentials, AuthProvider
from app.domain.ports.token_service import TokenPair, TokenService


class LoginUser:
    def __init__(self, auth: AuthProvider, tokens: TokenService) -> None:
        self._auth = auth
        self._tokens = tokens

    async def execute(
        self,
        *,
        email: str | None,
        phone: str | None,
        password: str,
    ) -> tuple[TokenPair, User]:
        credentials = AuthCredentials(email=email, phone=phone, password=password)
        user = await self._auth.authenticate(credentials)
        return self._tokens.create_tokens(user.id), user
