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


class Token(BaseModel):
    """
    JWT 토큰 응답 스키마
    """
    access_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True
