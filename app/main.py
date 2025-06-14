# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.v1.router import api_router
from app.core.config import settings 
from app.db.base import Base
from app.db.session import engine


# FastAPI 인스턴스 생성
app = FastAPI(
    title="FastAPI Board Backend",
    description="게시글, 파일 업로드, 댓글, 대댓글, 회원 기능을 포함한 백엔드 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS 설정 (필요에 따라 origins 수정)
origins = [
    "http://localhost",
    "http://localhost:3000", # 배포시 프론트엔드 주소 - maybe?
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 라우터 등록
app.include_router(api_router, prefix="/api/v1")

# 루트 접속시 문서 페이지로 리다이렉트 (선택)
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# 이벤트 핸들러: 예시로 DB 커넥션 풀 등 초기화 가능
@app.on_event("startup")
async def on_startup():
    ##################################################################
    # ↓ 아래는 개발·테스트 환경에서만 사용! 운영 중 변동 시 Alembic 사용 권장! ↓ #
    # Base.metadata.create_all(bind=engine)                          #
    # ↑ 위는 DDL을 실행함!!!!!!! 한 번만 실행하고 다음에는 반드시 주석 처리!!! ↑ #
    ##################################################################

    # 이후 동작을 지정하거나, 없으면 그냥 pass하거나...
    # 예) DB 연결 풀 초기화, 외부 서비스 연결, 캐시 warm-up 등
    pass

@app.on_event("shutdown")
async def on_shutdown():
    # 예) 커넥션 풀 정리, 임시 파일 정리 등
    pass
