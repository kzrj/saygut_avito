from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.config import settings
from app.domain.exceptions import UnauthorizedError
from app.domain.ports.token_service import TokenPair, TokenPayload, TokenService

ALGORITHM = "HS256"


class JwtTokenService(TokenService):
    def _encode(self, payload: dict, expires_delta: timedelta) -> str:
        data = payload.copy()
        data["exp"] = datetime.utcnow() + expires_delta
        return jwt.encode(data, settings.jwt_secret, algorithm=ALGORITHM)

    def create_tokens(self, user_id: str) -> TokenPair:
        access = self._encode(
            {"sub": user_id, "type": "access"},
            timedelta(minutes=settings.jwt_access_ttl_min),
        )
        refresh = self._encode(
            {"sub": user_id, "type": "refresh"},
            timedelta(days=settings.jwt_refresh_ttl_days),
        )
        return TokenPair(access_token=access, refresh_token=refresh)

    def _decode(self, token: str, expected_type: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
            if payload.get("type") != expected_type:
                raise UnauthorizedError("Invalid token type")
            return TokenPayload(sub=payload["sub"], type=payload["type"])
        except JWTError as e:
            raise UnauthorizedError("Invalid token") from e

    def decode_access(self, token: str) -> TokenPayload:
        return self._decode(token, "access")

    def decode_refresh(self, token: str) -> TokenPayload:
        return self._decode(token, "refresh")

    def refresh_tokens(self, refresh_token: str) -> TokenPair:
        payload = self.decode_refresh(refresh_token)
        return self.create_tokens(payload.sub)
