# config.py
from pydantic import MySQLDsn
from pydantic.v1 import BaseSettings

class AppSettings(BaseSettings):
    DEBUG: bool = True
    OPENAPI_URL: str | None = "/openapi.json" if DEBUG else None
    API_PREFIX: str = "/api"
    # DB_URL: MySQLDsn = "mysql+pymysql://admin:root@127.0.0.1:3306/admin"
    DB_URL: str  # 기본값 없이! (아예 이거 자체가 없으면 에러)
    TIMEZONE_LOCATION: str = "Asia/Seoul"
    DB_URL: str  # 기본값 없이! (아예 이거 자체가 없으면 에러)
    ALGORITHM: str = "HS256"
 
    AWS_ACCESS_KEY_ID: str = "myawsaccesskeyid"
    AWS_SECRET_ACCESS_KEY: str = "myawssecretaccesskey"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
 
settings = AppSettings()
