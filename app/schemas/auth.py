# app/schemas/auth.py

from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    """
    회원 가입 요청 스키마
    """
    username: str
    lastname: str
    firstname: str
    email: EmailStr
    password: str


class SignUpResponse(BaseModel):
    """
    회원 가입 성공 응답 스키마
    """
    user_id: int = Field(..., alias="userId")
    username: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class LoginRequest(BaseModel):
    """
    로그인 요청 스키마
    """
    username: str
    password: str


class TokenPair(BaseModel):
    """
    로그인 & 리프레시 응답: access + refresh
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True

class RefreshToken(BaseModel):
    """
    Refresh + access token 쌍을 요청하기 위한 스키마
    """
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True