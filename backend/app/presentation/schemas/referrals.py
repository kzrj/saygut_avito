from pydantic import BaseModel


class ReferralMeResponse(BaseModel):
    code: str
    invited_count: int
    earned_coins: int


class ReferralLinkResponse(BaseModel):
    url: str
