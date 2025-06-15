# 게시판 백엔드 프로젝트 (Windows 환경 안내)

FastAPI + MySQL 기반 다중 게시판 REST API 서버 프로젝트입니다.

---

## 요구사항

- Python 3.10 이상
- MySQL 8.0 이상
- 가상환경(venv) 사용 권장

---

## 1. 프로젝트 클론 및 가상환경 설정

```powershell
git clone <레포지토리_URL>
cd <프로젝트_폴더>
python -m venv venv
venv\Scripts\activate
```

---

## 2. 의존성 설치

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. 환경 변수 설정

- `.env.example`을 참고하여 `.env` 파일을 생성하세요.
- `app/core/config.py`의 환경 변수들을 구성하세요.

---

## 4. 데이터베이스 준비

MySQL에 접속하여 데이터베이스를 생성합니다.

```sql
CREATE DATABASE <데이터베이스명> CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 5. 마이그레이션 적용 (Alembic)

```powershell
alembic upgrade head
```

---

## 6. 서버 실행

```powershell
uvicorn app.main:app --reload
```

서버가 `http://localhost:8000` 에서 실행됩니다.

---

## 7. API 문서 확인

웹 브라우저에서 다음 주소에 접속하세요.

```
http://localhost:8000/docs
```

---

## 8. 주요 명령어

| 명령어                             | 설명                    |
|----------------------------------|-------------------------|
| `uvicorn app.main:app --reload`  | 개발용 서버 실행         |
| `alembic revision --autogenerate -m "메시지"` | 마이그레이션 생성  |
| `alembic upgrade head`            | 최신 마이그레이션 적용    |

---

## 문의

프로젝트 관련 문의는 GitHub 이슈나 이메일로 연락 부탁드립니다.
