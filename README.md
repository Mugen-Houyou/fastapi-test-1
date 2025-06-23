# 게시판 백엔드 프로젝트

FastAPI + MySQL + Redis 기반으로 구성한 게시판 & 실시간 채팅 서비스 백엔드입니다.

## 아키텍처 및 디자인 패턴

도메인과 기능 확장을 고려해서 아래와 같은 계층 구조로 구성하였습니다.

| 계층 | 설명 |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| **API (endpoint)**                       | FastAPI 엔드포인트 정의                                                    |
| **Service**                              | 비즈니스 로직/권한/파일 처리                                                  |
| **CRUD**                                 | DB 트랜잭션 처리 (SQLAlchemy ORM)                                          |
| **Schema**                               | 요청/응답 DTO (Pydantic)                                                  |
| **Model**                                | ORM 모델 (SQLAlchemy)                                                    |
| **Core/Deps**                            | 보안, JWT, 의존성 주입 (`HTTPBearer`/`OAuth2PasswordBearer` 등)                 |
| **Tests**                                | 기능 추가 및 변동에 따른 테스트 자동화                                                  |


디자인 패턴 관점에서 아래와 같습니다.

| 적용한 설계                                   | 설명                                                                      |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| **Repository Pattern**                   | `crud/` 하위에 DB 접근 로직을 캡슐화해 서비스 로직과 분리                                   |
| **Service Layer Pattern**                | 인증, 권한, 파일 저장 등 비즈니스 로직을 service 계층에 모아 단일 책임 원칙(SRP) 유지                |
| **DTO Pattern (Pydantic)**               | 입력/출력 스키마를 분리해서 내부 모델 은닉 및 검증 수행                                        |
| **Dependency Injection**                 | `Depends(get_db)`, `Depends(get_current_user)` 등을 통해 의존성 주입으로 느슨한 결합 유지 |
| **Forward Declaration & TYPE\_CHECKING** | 순환 참조를 피하면서 ORM 관계를 안전하게 정의                                             |


---

## 0. 요구사항

- Python 3.11 이상
- MySQL 서버 8.0 이상
- Redis 서버 6.0 이상 (AUTH 비밀번호 사용 권장)
- Poetry 또는 pip (가상환경 권장)

---

## 1. 프로젝트 클론 및 가상환경 설정

- **POSIX-compliant (macOS, Linux 등)**:

```bash
cd <이_프로젝트_폴더>
python -m venv venv
source venv/bin/activate
```

- **Windows**:

```powershell
cd <이_프로젝트_폴더>
python -m venv venv
venv\Scripts\activate
```

---

## 2. 의존성 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

또는 Poetry 사용 시

```bash
poetry install
```

---

## 3. 환경변수 설정

- `.env.example`을 참고하여 `.env` 파일을 생성하세요.
- `app/core/config.py`의 환경 변수들을 구성하세요.
- Redis 서버를 실행할 때는 반드시 인증 비밀번호(`requirepass`)를 설정하고
  `.env`의 `REDIS_AUTH_PASSWORD` 값과 동일하게 맞춰 주세요.

---

## 4. DB 준비

MySQL 기준으로, 아래와 같은 식으로 DB를 생성하세요.

```
CREATE DATABASE <데이터베이스명> CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 5. DB 마이그레이션 (Alembic 등)

선택 사항입니다.

```
alembic upgrade head
```

---

## 6. 서버 실행

```
uvicorn app.main:app --reload
```

서버가 `http://localhost:8000` 에서 실행됩니다.

---

## 7. API 문서 확인

웹 브라우저로 다음 주소에 접속하세요.

```
http://localhost:8000/docs
```

참고: 실시간 채팅 (WebSocket)을 테스트하려면 `README.websocket.md`을 확인하세요. **현재 채팅 기록은 Redis에만 담기며**, 이를 MySQL에 보존시키는 기능은 계획 중에 있습니다.

---

## 8. 주요 명령어

| 명령어                             | 설명                    |
|----------------------------------|-------------------------|
| `uvicorn app.main:app --reload`  | 개발용 서버 실행         |
| `alembic revision --autogenerate -m "메시지"` | 마이그레이션 생성  |
| `alembic upgrade head`            | 최신 마이그레이션 적용    |

---

## 문의

프로젝트 관련 문의는 GitHub 이슈나 이메일로 부탁 드립니다.
