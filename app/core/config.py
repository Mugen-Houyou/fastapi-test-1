# config.py
from pydantic import MySQLDsn
from pydantic.v1 import BaseSettings

class AppSettings(BaseSettings):
    DEBUG: bool = True
    
    OPENAPI_URL: str | None = "/openapi.json" if DEBUG else None
    API_PREFIX: str = "/api"
    # DB_URL: MySQLDsn = "mysql+pymysql://admin:root@127.0.0.1:3306/admin"
    DB_URL: str  # 타입만 지정!
    TIMEZONE_LOCATION: str = "Asia/Seoul"

    JWT_ACCESS_SECRET_KEY: str  # 타입만 지정!
    JWT_REFRESH_SECRET_KEY: str  # 타입만 지정!
    JWT_AC_MINS: int = 120 # Access token의 유효 시간 (단위: 분)
    JWT_RF_DAYS: int = 180 # Refresh token의 유효 기간 (단위: 일)
    ALGORITHM: str = "HS256"
 
    AWS_ACCESS_KEY_ID: str = "myawsaccesskeyid"
    AWS_SECRET_ACCESS_KEY: str = "myawssecretaccesskey"

    class Config: # 이 오류는 무시해도 ㄱㅊ
        env_file = ".env"
        env_file_encoding = "utf-8"
    
 
settings = AppSettings()
