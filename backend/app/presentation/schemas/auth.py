from pydantic import BaseModel, EmailStr, Field, model_validator


class RegisterRequest(BaseModel):
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=10, max_length=20)
    password: str = Field(min_length=6, max_length=128)
    password_confirm: str | None = Field(default=None, min_length=6)
    display_name: str | None = Field(default=None, max_length=100)
    referral_code: str | None = Field(default=None, max_length=20)

    @model_validator(mode="after")
    def validate_register(self) -> "RegisterRequest":
        if not self.email and not self.phone:
            raise ValueError("Укажите email или телефон")
        if self.password_confirm is not None and self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")
        if self.referral_code:
            self.referral_code = self.referral_code.strip().upper()
        return self


class LoginRequest(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    password: str

    @model_validator(mode="after")
    def require_login(self) -> "LoginRequest":
        if not self.email and not self.phone:
            raise ValueError("Email or phone is required")
        return self


class RefreshRequest(BaseModel):
    refresh_token: str


class UserProfile(BaseModel):
    id: str
    email: str | None
    phone: str | None
    display_name: str
    wallet_balance: int
    referral_code: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserProfile


class AuthResponse(TokenResponse):
    pass
