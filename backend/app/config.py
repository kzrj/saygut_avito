from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mongodb_url: str = "mongodb://mongodb:27017"
    mongodb_db: str = "microavito"
    jwt_secret: str = "change-me"
    jwt_access_ttl_min: int = 30
    jwt_refresh_ttl_days: int = 30
    listing_fee_coins: int = 10
    rub_per_coin: int = 10
    yoomoney_shop_id: str = ""
    yoomoney_secret: str = ""
    yoomoney_return_url: str = "http://localhost:8081/wallet"
    referral_bonus_coins: int = 5
    referral_reward_on: str = "first_publish"
    enable_admin_credit: bool = True
    enable_escrow: bool = False
    enable_barter: bool = False
    upload_dir: str = "/app/uploads"
    app_public_url: str = "http://localhost:8081"


settings = Settings()
