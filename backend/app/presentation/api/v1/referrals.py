from fastapi import APIRouter, Depends

from app.domain.entities.user import User
from app.presentation.container import container
from app.presentation.deps import get_current_user
from app.presentation.schemas.referrals import ReferralLinkResponse, ReferralMeResponse

router = APIRouter(prefix="/referrals", tags=["referrals"])


@router.get("/me", response_model=ReferralMeResponse)
async def referral_me(user: User = Depends(get_current_user)):
    stats = await container.get_referral_stats.execute(user.id)
    return ReferralMeResponse(
        code=stats.code,
        invited_count=stats.invited_count,
        earned_coins=stats.earned_coins,
    )


@router.get("/link", response_model=ReferralLinkResponse)
async def referral_link(user: User = Depends(get_current_user)):
    stats = await container.get_referral_stats.execute(user.id)
    return ReferralLinkResponse(url=stats.link)
