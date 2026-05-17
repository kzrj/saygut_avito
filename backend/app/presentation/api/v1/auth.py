from fastapi import APIRouter, Depends, Request, Response
from app.presentation.limiter import limiter

from app.domain.exceptions import DomainError
from app.domain.entities.user import User
from app.presentation.container import container
from app.presentation.deps import get_current_user, user_to_profile
from app.presentation.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserProfile,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
@limiter.limit("20/minute")
async def register(request: Request, body: RegisterRequest):
    try:
        tokens, user = await container.register_user.execute(
            email=body.email,
            phone=body.phone,
            password=body.password,
            display_name=body.display_name,
            referral_code=body.referral_code,
        )
    except DomainError as e:
        from fastapi import HTTPException

        status_code = 409 if e.code == "conflict" else 400
        raise HTTPException(status_code=status_code, detail=e.message) from e
    return AuthResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        user=UserProfile(**user_to_profile(user)),
    )


@router.post("/login", response_model=AuthResponse)
@limiter.limit("30/minute")
async def login(request: Request, body: LoginRequest):
    try:
        tokens, user = await container.login_user.execute(
            email=body.email,
            phone=body.phone,
            password=body.password,
        )
    except DomainError as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail=e.message) from e
    return AuthResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        user=UserProfile(**user_to_profile(user)),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest):
    from fastapi import HTTPException
    from app.domain.exceptions import UnauthorizedError

    try:
        tokens = container.tokens.refresh_tokens(body.refresh_token)
        user = await container.get_current_user.execute(
            container.tokens.decode_refresh(body.refresh_token).sub
        )
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=e.message) from e
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        user=UserProfile(**user_to_profile(user)),
    )


@router.get("/me", response_model=UserProfile)
async def me(user: User = Depends(get_current_user)):
    return UserProfile(**user_to_profile(user))


@router.post("/logout", status_code=204)
async def logout():
    return Response(status_code=204)
