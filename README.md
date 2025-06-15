# 게시판 백엔드 프로젝트

FastAPI + MySQL 기반 다중 게시판 REST API 서버 프로젝트입니다.

---

## 요구사항

- Python 3.10 이상
- MySQL 8.0 이상
- Poetry 또는 pip (가상환경 권장)

---

## 1. 프로젝트 클론 및 가상환경 설정

```bash
git clone <레포지토리_URL>
cd <프로젝트_폴더>
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
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

`.env.example`을 참고하여 `.env` 파일을 생성하세요. 

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

---

## 7. Docs 참조

http://localhost:8000/docs



