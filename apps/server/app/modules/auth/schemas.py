from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterOrganizationRequest(BaseModel):
    organization_name: str = Field(
        min_length=2,
        max_length=255,
    )

    owner_first_name: str = Field(
        min_length=2,
        max_length=100,
    )

    owner_last_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    phone: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    first_name: str
    last_name: str
    organization: str
    role: str


class LoginRequest(BaseModel):
    email: EmailStr

    password: str


class AuthUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    first_name: str
    last_name: str
    organization: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: AuthUserResponse
