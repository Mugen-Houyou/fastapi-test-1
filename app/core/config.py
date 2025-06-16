# app/core/config.py

"""
각 설정값의 타입과 함께, 민감하지 않은 설정값을 지정.
민감한 설정값의 경우 `.env` 파일에 별도로 저장 (예시는 `.env.example` 참조).
"""

# from pydantic import MySQLDsn # 혹시 MySQLDsn 등을 쓰려면 주석 해제할 것.
from pathlib import Path
from pydantic.v1 import BaseSettings

class AppSettings(BaseSettings):
    DEBUG: bool = True
    
    OPENAPI_URL: str | None = "/openapi.json" if DEBUG else None
    API_PREFIX: str = "/api"
    TIMEZONE_LOCATION: str = "Asia/Seoul"

    FILE_STORAGE_DIR: Path = Path("./uploads")  # 절대/상대경로 모두 가능... 지금은 상대 경로로.
    MAX_UPLOAD_MB: int = 20 # 업로드 최대 사이즈 (단위: MB)

    DB_URL: str  # 타입만 지정! 실제 값은 `.env`에! 혹시 MySQLDsn 등을 쓰려면, `MySQLDsn = "mysql+pymysql://admin:root@127.0.0.1:3306/admin"` 같은 식으로.
    DB_TEST_URL: str  # 타입만 지정! 실제 값은 `.env`에!

    JWT_ACCESS_SECRET_KEY: str  # 타입만 지정! 실제 값은 `.env`에!
    JWT_REFRESH_SECRET_KEY: str  # 타입만 지정! 실제 값은 `.env`에!
    JWT_AC_MINS: int = 120 # Access token의 유효 시간 (단위: 분)
    JWT_RF_DAYS: int = 180 # Refresh token의 유효 기간 (단위: 일)
    ALGORITHM: str = "HS256"

    REDIS_URL: str  # 타입만 지정! 실제 값은 `.env`에!
    REDIS_AUTH_PASSWORD: str # 타입만 지정! 실제 값은 `.env`에!
 
    AWS_ACCESS_KEY_ID: str = "myawsaccesskeyid" # TODO: `.env`로 따로 뺀 뒤 타입만 지정!
    AWS_SECRET_ACCESS_KEY: str = "myawssecretaccesskey" # TODO: `.env`로 따로 뺀 뒤 타입만 지정!

    class Config: # 이 오류는 무시해도 ㄱㅊ
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    
settings = AppSettings()
