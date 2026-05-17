from fastapi import APIRouter

from app.presentation.api.v1 import auth, listings, payments, referrals, wallet

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth.router)
api_router.include_router(wallet.router)
api_router.include_router(listings.router)
api_router.include_router(payments.router)
api_router.include_router(referrals.router)
