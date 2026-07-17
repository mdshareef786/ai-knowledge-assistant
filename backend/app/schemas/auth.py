from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RegisterRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user"
    )

    email: EmailStr = Field(
        ...,
        description="Valid email address of the user"
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password must contain between 8 and 72 characters"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "user",
                "email": "user@example.com",
                "password": "Password@123"
            }
        }
    )


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Registered email address"
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="User password"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "Password@123"
            }
        }
    )

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Registered email address"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com"
            }
        }
    )


class ResetPasswordRequest(BaseModel):
    token: str = Field(
        ...,
        min_length=1,
        description="Password reset token"
    )

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="New password must contain between 8 and 72 characters"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "password-reset-token",
                "new_password": "NewPassword@123"
            }
        }
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer"
            }
        }
    )